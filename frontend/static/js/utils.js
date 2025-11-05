export function formatCurrency(v){ return new Intl.NumberFormat('en-IN', { style:'currency', currency:'INR' }).format(v); }
export function daysBetween(a,b){ return Math.round((new Date(b)-new Date(a))/(1000*60*60*24)); }
export function uid(prefix='ID'){ return prefix + '-' + Math.random().toString(36).slice(2,9).toUpperCase(); }
