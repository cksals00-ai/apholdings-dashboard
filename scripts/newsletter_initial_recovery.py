"""Recover source-bound failed copy; never regenerate accepted drafts or assets."""
import hashlib,json,re
from newsletter_grounding import indexed_source,resolve_evidence,retain_source_product_names,validate_source_copy
import newsletter_schemas as shapes

def recover_product_drafts(folder,state,sources,save):
 from pathlib import Path
 by_url={s['url']:s for s in sources};existing={s['url'] for s in state['stories']}
 affected={h['source']['url'] for h in state.get('copy_history',[]) if h.get('reason','').startswith('Keep original product name in Latin spelling:') and isinstance(h.get('source'),dict) and h['source'].get('url') in by_url}
 files=list((Path(folder)/'model-outputs').glob('*.json'))
 def sequence(path):
  suffix=path.stem.rsplit('-',1)[-1];return int(suffix) if suffix.isdigit() else 0
 for path in sorted(files,key=sequence,reverse=True):
  if len(state['stories'])>=5:return
  try:
   raw=json.loads(path.read_text());runtime=raw['_ap_runtime'];prompt=raw['prompt']
   if runtime.get('profile')!='copy' or not isinstance(prompt,str) or hashlib.sha256(('copy\n'+prompt).encode()).hexdigest()!=runtime.get('prompt_sha256'):continue
   begin=prompt.index('<source_data>')+len('<source_data>');context,_=json.JSONDecoder().raw_decode(prompt[begin:])
   url=context.get('url');source=by_url.get(url)
   if url not in affected or url in existing or source is None:continue
   if hashlib.sha256(source['text'].encode()).hexdigest()!=source['body_sha256'] or context!=indexed_source(source):continue
   wire=json.loads(raw['content'])
   if not isinstance(wire,dict) or set(wire)!=set(shapes.DRAFT_INDEXED['properties']):continue
   draft=retain_source_product_names(resolve_evidence(wire,context),source)
   validate_source_copy(draft,source)
   # This draft has no semantic approval. The mandatory independent verifier
   # must evaluate all fields; retained old weak outputs cannot publish it.
   draft.update(url=url,source=source['source'],published=source['published'],source_hash=source['body_sha256'],review={'supported':False,'unsupported_claims':['Pending independent source review after original-name formatting']})
   state['stories'].append(draft);existing.add(url)
   state.setdefault('recovered_initial_drafts',[]).append({'url':url,'raw_receipt':path.name,'raw_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_hash':source['body_sha256'],'method':'source-bound original-name label; no factual approval'})
  except (ValueError,KeyError,TypeError,AttributeError):continue
  save()
