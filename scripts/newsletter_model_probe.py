"""Benchmark public local weights on the production runner, without AI API keys."""
import json,os,time,subprocess,urllib.request
from pathlib import Path
from huggingface_hub import hf_hub_download
out=Path('probe-output');out.mkdir(exist_ok=True)
start=time.monotonic()
model=hf_hub_download('Qwen/Qwen3-4B-GGUF','Qwen3-4B-Q4_K_M.gguf',revision='bc640142c66e1fdd12af0bd68f40445458f3869b',token=False)
server=next(Path('.cpu-runtime').rglob('llama-server'))
log=(out/'text-runtime.log').open('w')
runtime_env=dict(os.environ,LD_LIBRARY_PATH=':'.join(sorted({str(p.parent.resolve()) for p in Path('.cpu-runtime').rglob('*.so*')})))
proc=subprocess.Popen([str(server.resolve()),'-m',model,'-c','8192','-t','2','-ngl','0','--host','127.0.0.1','--port','8080'],stdout=log,stderr=log,env=runtime_env)
try:
 for _ in range(180):
  try:
   if urllib.request.urlopen('http://127.0.0.1:8080/health',timeout=2).status==200:break
  except Exception:
   if proc.poll() is not None:raise RuntimeError('CPU text runtime exited')
   time.sleep(1)
 else:raise TimeoutError('CPU model startup')
 prompt='''<|im_start|>system
You edit AP Holdings AI news in Korean. Return only JSON with title,summary,fact,insight,action. Facts must use only the supplied source. Do not invent metrics, availability or claims. Insight is an AP business interpretation, not another reported fact.<|im_end|>
<|im_start|>user
Official source: Google announced on October 29, 2026 that people can create and edit documents, spreadsheets and presentations directly in the Gemini app. Users can preview files and request revisions in the same conversation. Write concise, natural Korean; mention only these supplied facts. AP provides AI education, content and web services. /no_think<|im_end|>
<|im_start|>assistant
<think>\n\n</think>\n\n'''
 t=time.monotonic()
 data=json.dumps({'prompt':prompt,'n_predict':900,'temperature':0.2,'stop':['<|im_end|>'],'cache_prompt':False}).encode()
 with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8080/completion',data=data,headers={'Content-Type':'application/json'}),timeout=1200) as r:result=json.load(r)
 (out/'text.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 metrics={'text_seconds':time.monotonic()-t,'text_total_seconds':time.monotonic()-start,'cpu_threads':2}
finally:
 proc.terminate();proc.wait(timeout=30);log.close()
import torch
from diffusers import StableDiffusionPipeline
threads=min(2,os.cpu_count() or 2);torch.set_num_threads(threads)
t=time.monotonic()
pipe=StableDiffusionPipeline.from_pretrained('segmind/tiny-sd',revision='cad0bd7495fa6c4bcca01b19a723dc91627fe84f',torch_dtype=torch.float32,token=False)
pipe=pipe.to('cpu');pipe.enable_attention_slicing()
image=pipe('Editorial gouache illustration, person thoughtfully editing floating document pages at an ivory desk, side view, deep navy and sage accents, refined brass detail, bold painterly brush marks, calm generous composition, conceptual illustration, no text, no logo, no photograph',negative_prompt='text, letters, watermark, logo, photorealistic, deformed hands, blurry',num_inference_steps=16,guidance_scale=7.5,width=768,height=512,generator=torch.Generator('cpu').manual_seed(311026)).images[0]
image.save(out/'image.png');metrics['image_seconds']=time.monotonic()-t;metrics['total_seconds']=time.monotonic()-start
(out/'metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics),flush=True)
