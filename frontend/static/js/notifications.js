export function notify(title, body){
  if("Notification" in window && Notification.permission === "granted"){
    new Notification(title, { body });
  } else if("Notification" in window && Notification.permission !== "denied"){
    Notification.requestPermission().then(p => { if(p === 'granted') new Notification(title,{body}); });
  } else {
    // fallback toast
    window.toast(title + ' — ' + body);
  }
}
