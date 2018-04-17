import axios from 'axios';


export default function getData(successHandler, errorHandler) {
  axios.get('/ws/v1/shootings')
    .then(function(response) {
      successHandler(response);
    })
    .catch(function(error) {
      errorHandler(error);
    })
}