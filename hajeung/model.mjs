const text=(v,min,max,label)=>{const s=String(v??'').trim();if(s.length<min||s.length>max)throw Error(`${label}: ${min}~${max}자로 입력해 주세요.`);return s;};
const choice=(v,values)=>{if(!values.includes(v))throw Error('선택 항목을 확인해 주세요.');return v;};
export const application=x=>({name:text(x.name,1,60,'이름'),company:text(x.company,1,100,'회사·소속'),device:choice(x.device,['ios','android','both'])});
export const request=x=>({kind:choice(x.kind,['bug','improvement','question']),title:text(x.title,2,120,'제목'),body:text(x.body,5,4000,'내용'),screen:text(x.screen,0,100,'발생 화면'),version:text(x.version,0,80,'앱 버전'),device:text(x.device,0,120,'기기·OS')});
export function attachment(file){if(!['image/jpeg','image/png','image/webp'].includes(file.type)||file.size<1||file.size>5*1024*1024)throw Error('사진은 JPG·PNG·WebP, 5MB 이하로 선택해 주세요.');return file;}
export const labels={pending:'접수',approved:'승인 · 앱 코드 발급 대기',held:'보류',rejected:'승인 불가',issued:'앱 코드 발급됨',received:'접수',reviewing:'확인 중',working:'처리 중',needs_info:'추가 정보 요청',done:'완료'};
export const statusLabel=s=>labels[s]||'확인 필요';
