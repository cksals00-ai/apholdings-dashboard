"""Fail-closed structural and source-evidence checks for model-written copy."""
import json,re,unicodedata
from decimal import Decimal

def parse_json(text):
 text=re.sub(r'^```(?:json)?\s*|\s*```$','',text.strip())
 try:
  result=json.loads(text)
  if not isinstance(result,dict):raise ValueError('Expected a JSON object')
  return result
 except (ValueError,TypeError) as exc:raise ValueError('Model did not return a JSON object') from exc

def normalized(text):return ' '.join(unicodedata.normalize('NFKC',text).translate(str.maketrans({'’':"'",'‘':"'",'“':'"','”':'"','–':'-','—':'-'})).split())
def numbers(text):
 # Normalize standalone cardinal words without treating ordinals/categories as equivalent.
 words='zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split()
 vocabulary=words+'thirty forty fifty sixty seventy eighty ninety hundred thousand million billion first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth thirteenth fourteenth fifteenth sixteenth seventeenth eighteenth nineteenth twentieth thirtieth fortieth fiftieth sixtieth seventieth eightieth ninetieth hundredth thousandth'.split()
 word_pattern=r'\b(?:'+ '|'.join(vocabulary) +r')\b'
 result=set()
 for phrase in re.findall(word_pattern+r'(?:[ -]+(?:and[ -]+)?'+word_pattern+r')*',text,re.I):
  if phrase.lower() in words:result.add(str(words.index(phrase.lower())))
 for raw in re.findall(r'\d+(?:[.,]\d+)*(?:%|[BMK])?',text):
  suffix=raw[-1] if raw[-1] in '%BMK' else '';value=raw[:-1] if suffix else raw
  if re.fullmatch(r'\d{1,3}(?:,\d{3})+(?:\.\d+)?',value):value=value.replace(',','')
  try:value=format(Decimal(value).normalize(),'f')
  except Exception:pass
  result.add(value+suffix)
 return result
def validate_grounding(story,source,review):
 for key in ('title','summary','fact','insight','action','image_prompt','image_subject','visual_approach'):
  value=story.get(key)
  if not isinstance(value,str) or not value.strip() or len(value)>1800:raise ValueError('Invalid editorial field: '+key)
 if len(story['image_prompt'])>650 or len(story['image_subject'])>120:raise ValueError('Image plan too long')
 for key in ('title','summary','fact','insight','action'):
  if not re.search('[가-힣]',story[key]):raise ValueError('Korean copy required in '+key+'; keep only product/company names in Latin spelling')
 if len(story['title'])>90 or len(story['summary'])>180:raise ValueError('Unusable headline/summary length')
 quotes=story.get('evidence')
 if not isinstance(quotes,list) or not 1<=len(quotes)<=4:raise ValueError('Original evidence quotes required')
 text=normalized(source['text'])
 for quote in quotes:
  if not isinstance(quote,str) or len(quote)<30 or len(quote)>900 or normalized(quote) not in text:raise ValueError('Evidence quote is not in official source; copy literal English without translating or adding particles: '+str(quote)[:140])
 copy=' '.join(story[k] for k in ('title','summary','fact'))
 for name in ('Gemini','Notebook','Copilot','Claude','ChatGPT','AgentCore','Nemotron','Bedrock'):
  if re.search(r'\b'+re.escape(name)+r'\b',source.get('title',''),re.I) and name.lower() not in copy.lower():raise ValueError('Keep original product name in Latin spelling: '+name)
 # Only verbatim evidence can authorize new factual figures; source date is displayed separately.
 evidence=' '.join(quotes)
 for key in ('title','summary','fact'):
  missing=numbers(story[key])-numbers(evidence)
  if missing:raise ValueError('Unsupported numeric claim in '+key+': '+', '.join(sorted(missing))+'; remove the claim or quote exact supporting source text')
 if review.get('supported') is not True or review.get('unsupported_claims')!=[]:raise ValueError('Independent source review rejected draft: '+str(review.get('unsupported_claims',[])))
 if any(term in story['fact'] for term in ('사람이 검수','전문가 검수','수동 검수')):raise ValueError('False human-review claim')
 return True
