"""Fail-closed structural and source-evidence checks for model-written copy."""
import json,re

def parse_json(text):
 text=re.sub(r'^```(?:json)?\s*|\s*```$','',text.strip())
 try:
  result=json.loads(text)
  if not isinstance(result,dict):raise ValueError('Expected a JSON object')
  return result
 except (ValueError,TypeError) as exc:raise ValueError('Model did not return a JSON object') from exc

def normalized(text):return ' '.join(text.split())
def numbers(text):return set(re.findall(r'\d+(?:[.,]\d+)*(?:%|[BMK])?',text))
def validate_grounding(story,source,review):
 for key in ('title','summary','fact','insight','action','image_prompt','image_subject','visual_approach'):
  value=story.get(key)
  if not isinstance(value,str) or not value.strip() or len(value)>1800:raise ValueError('Invalid editorial field: '+key)
 if len(story['image_prompt'])>650 or len(story['image_subject'])>120:raise ValueError('Image plan too long')
 for key in ('title','summary','fact','insight','action'):
  if not re.search('[가-힣]',story[key]):raise ValueError('Korean copy required')
 if len(story['title'])>90 or len(story['summary'])>180:raise ValueError('Unusable headline/summary length')
 quotes=story.get('evidence')
 if not isinstance(quotes,list) or not 1<=len(quotes)<=4:raise ValueError('Original evidence quotes required')
 text=normalized(source['text'])
 for quote in quotes:
  if not isinstance(quote,str) or len(quote)<30 or len(quote)>900 or normalized(quote) not in text:raise ValueError('Evidence quote is not in official source')
 # Only verbatim evidence can authorize new factual figures; source date is displayed separately.
 evidence=' '.join(quotes)
 for key in ('title','summary','fact'):
  if numbers(story[key])-numbers(evidence):raise ValueError('Unsupported numeric claim')
 if review.get('supported') is not True or review.get('unsupported_claims')!=[]:raise ValueError('Independent source review rejected draft')
 if any(term in story['fact'] for term in ('사람이 검수','전문가 검수','수동 검수')):raise ValueError('False human-review claim')
 return True
