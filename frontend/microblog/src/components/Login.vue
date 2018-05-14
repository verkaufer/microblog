<template>
  <div>
    <b-row class="justify-content-center">
      <b-col md="8">
          <h2>Please Log In</h2>
          <div v-show="form.errors.length > 0">
            <b-alert v-for="(errorMsg, index) in form.errors" show variant="danger">
              {{ errorMsg.details }}
            </b-alert>
          </div>
          <b-form @submit.prevent="login">
            <b-form-group id="username"
                          label="Username">
              <b-form-input id="username"
                            type="text"
                            v-model="form.username"
                            required
                            placeholder="Username">
              </b-form-input>
            </b-form-group>
            <b-form-group id="password"
                          label="Password">
              <b-form-input id="password"
                            type="password"
                            v-model="form.password"
                            required
                            placeholder="Password">
              </b-form-input>
            </b-form-group>
            <b-button type="submit" :disabled="submittingForm" variant="primary">Submit</b-button>
          </b-form>
        <hr>
        <p>No account? <router-link to="/signup">Sign up here</router-link></p>
        </b-col>
    </b-row>
  </div>
</template>

<script>
import AuthenticationService from '@/services/authentication'

  export default {
    name: 'login',
    data () {
      return {
        form: {
          username: '',
          password: '',
          errors: []
        },
        submittingForm: false
      }
    },
    methods: {
      login () {
        this.form.errors = []
        this.submittingForm = true
        const auth = new AuthenticationService();
        auth.login({username: this.form.username, password: this.form.password})
        .then((data) => this.$router.push('/home'))
        .catch((err) => {
          console.log(err);
            this.form.errors.push({
              'details': 'Unable to login with that username and password.',
              'code': 'login_failure'})
            this.form.password = ''
        })
        .then(() => {
            this.submittingForm = false
        })
      }
    }
  }
</script>

<style scoped>
</style>