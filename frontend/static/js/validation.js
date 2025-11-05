export function required(value){ return value !== null && value !== undefined && String(value).trim() !== ''; }
export function isEmail(value){ return /\S+@\S+\.\S+/.test(value); }
export function validateBooking(from,to){ return new Date(to) > new Date(from); }
