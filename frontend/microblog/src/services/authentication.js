import API from './requests'



export default class AuthenticationService {
    constructor() {}

    login(credentials) {
        return API.post('/auth/login/', credentials)
        // pass in username and password in credentials object
    }

    register(registration_info) {
        return API.post('/auth/login/', registration_info)
    }

    logout() {
        return API.get('/auth/logout/')
    }
}