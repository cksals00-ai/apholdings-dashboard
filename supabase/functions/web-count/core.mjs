const hosts=['www.apholdings.kr','apholdings.kr','edu.apholdings.kr','games.apholdings.kr','ent.apholdings.kr','shop.apholdings.kr','sports.apholdings.kr'];
export function validateCount(origin,body){
 let host;try{const u=new URL(origin);if(u.protocol!=='https:'||!hosts.includes(u.hostname)||u.port)return null;host=u.hostname;}catch{return null;}
 if(!body||typeof body!=='object'||Object.keys(body).some(k=>!['host','event'].includes(k))||body.host!==host)return null;
 if(!['page_view','courtmate_blog_arrival','ap_install_test'].includes(body.event))return null;
 if(body.event==='courtmate_blog_arrival'&&host!=='sports.apholdings.kr')return null;
 return {host,event:body.event};
}
