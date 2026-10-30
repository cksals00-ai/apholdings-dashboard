"""Public model weights executed in-process/on localhost. No hosted AI endpoints."""
import json,os,subprocess,time,urllib.request
from pathlib import Path
from newsletter_grounding import parse_json
TEXT_REPO='unsloth/Qwen3-4B-Instruct-2507-GGUF'
TEXT_REV='a06e946bb6b655725eafa393f4a9745d460374c9'
IMAGE_REPO='segmind/SSD-1B'
IMAGE_REV='60987f37e94cd59c36b1cba832b9f97b57395a10'
class TextModel:
 def __init__(self,runtime,folder):self.runtime=Path(runtime);self.folder=Path(folder);self.proc=None
 def __enter__(self):
  from huggingface_hub import hf_hub_download
  model=hf_hub_download(TEXT_REPO,'Qwen3-4B-Instruct-2507-Q4_K_M.gguf',revision=TEXT_REV,token=False)
  executable=next(self.runtime.rglob('llama-server'))
  env={k:os.environ[k] for k in ('PATH','HOME','LANG','LC_ALL','TMPDIR') if k in os.environ}
  env['LD_LIBRARY_PATH']=':'.join(sorted({str(p.parent.resolve()) for p in self.runtime.rglob('*.so*')}))
  self.log=(self.folder/'text-runtime.log').open('a')
  self.proc=subprocess.Popen([str(executable.resolve()),'-m',model,'-c','8192','-t','4','-ngl','0','--host','127.0.0.1','--port','8080'],stdout=self.log,stderr=self.log,env=env)
  try:
   for _ in range(180):
    try:
     if urllib.request.urlopen('http://127.0.0.1:8080/health',timeout=2).status==200:return self
    except Exception:
     if self.proc.poll() is not None:raise RuntimeError('CPU text runtime exited')
     time.sleep(1)
   raise TimeoutError('CPU text startup timeout')
  except Exception:
   self.__exit__(None,None,None);raise
 def __exit__(self,*_):
  if self.proc:
   self.proc.terminate();self.proc.wait(timeout=30)
  self.log.close()
 def ask(self,system,question,tokens=1400):
  prompt=f'<|im_start|>system\n{system}<|im_end|>\n<|im_start|>user\n{question}\n<|im_end|>\n<|im_start|>assistant\n'
  data=json.dumps({'prompt':prompt,'n_predict':tokens,'temperature':0.2,'stop':['<|im_end|>'],'cache_prompt':False}).encode()
  request=urllib.request.Request('http://127.0.0.1:8080/completion',data=data,headers={'Content-Type':'application/json'})
  with urllib.request.urlopen(request,timeout=1500) as response:result=json.load(response)
  if result.get('stopped_limit'):raise ValueError('Model generation reached token limit')
  return parse_json(result['content'])

class ImageModel:
 def __init__(self):
  import torch
  from diffusers import StableDiffusionXLPipeline,LCMScheduler
  torch.set_num_threads(4)
  self.pipe=StableDiffusionXLPipeline.from_pretrained(IMAGE_REPO,revision=IMAGE_REV,variant='fp16',torch_dtype=torch.float32,token=False).to('cpu')
  self.pipe.load_lora_weights('latent-consistency/lcm-lora-ssd-1b',revision='857c372dbe0edd8af6255638a68d0d7ccb7a3d76',token=False)
  self.pipe.scheduler=LCMScheduler.from_config(self.pipe.scheduler.config)
  self.pipe.enable_attention_slicing()
 def create(self,prompt,seed):
  import torch
  result=self.pipe(prompt+', conceptual editorial illustration, no text, no logo, not a product screenshot',negative_prompt='text, letters, watermark, logo, screenshot, photograph, photorealistic, blurry, deformed anatomy',num_inference_steps=6,guidance_scale=1.5,width=768,height=512,generator=torch.Generator('cpu').manual_seed(seed))
  if getattr(result,'nsfw_content_detected',None) and any(result.nsfw_content_detected):raise ValueError('Image safety check rejected output')
  return result.images[0]

class ImageSubjectCheck:
 def __init__(self):
  from transformers import CLIPModel,CLIPProcessor
  revision='3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268'
  self.model=CLIPModel.from_pretrained('openai/clip-vit-base-patch32',revision=revision,token=False).eval()
  self.processor=CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32',revision=revision,token=False)
 def check(self,image,subject):
  import torch
  unrelated=['flowers in a vase on an empty desk','a sports car on a road','a bowl of food','an empty chair and furniture','a mountain landscape','an unrelated generic circular orbit diagram']
  inputs=self.processor(text=[subject]+unrelated,images=image,return_tensors='pt',padding=True,truncation=True)
  with torch.no_grad():scores=self.model(**inputs).logits_per_image[0].tolist()
  return scores[0]>max(scores[1:]),{'subject':subject,'target_score':scores[0],'unrelated_scores':scores[1:]}
