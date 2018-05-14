import BASE_URL from './config'
import axios from 'axios'


/**
* Returns the value of a cookie for a given name
*/
let _getCookie = (name) => {  
  // source: https://stackoverflow.com/q/10730362/2291333
  const value = "; " + document.cookie;
  let parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

const baseAPIConfig = axios.create({
    baseURL: BASE_URL,
    timeout: 1000,
    headers: {'X-CSRFToken': _getCookie('csrftoken') }
})

export default baseAPIConfig