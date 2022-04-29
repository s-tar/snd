<template>
  <div class="card">
    <div class="card__header">
      <div class="card__title">Login</div>
    </div>
    <div class="card__body">
      <AsyncForm
        v-slot="form"
        action="/auth/login"
        method="post"
        class="form"
        :errors="errors"
        :is-success="isSuccess"
        :on-success="onSuccess"
        :on-error="onError"
      >
        <div class="form__row">
          <div class="form__col">
            <InputField id="email" type="email" name="username" label="Email" />
          </div>
        </div>
        <div class="form__row">
          <div class="form__col">
            <InputField id="password" type="password" name="password" label="Password" />
          </div>
        </div>
        <div class="form__row form__row--valign-center">
          <div class="form__col form__col--align-stretch">
            <a href="/auth/register" class="link">Register</a>
            <Submit type="submit" class="button button--success" :processing="form.processing">Login</Submit>
          </div>
        </div>
      </AsyncForm>
    </div>
  </div>
</template>

<script>
import AsyncForm from '~/components/AsyncForm'
import InputField from '~/components/AsyncForm/fields/Input'
import Submit from '~/components/AsyncForm/fields/Submit'
import { RESPONSE_STATUS } from '~/utils/response_status'

export default {
  auth: 'guest',
  components: {
    InputField,
    AsyncForm,
    Submit,
  },
  layout() {
    return 'simple'
  },
  data() {
    return {
      errors: {},
    }
  },
  methods: {
    isSuccess(response) {
      return response.data.status !== RESPONSE_STATUS.DATA_VALIDATION_FAILED
    },
    onSuccess(response) {
      if (response.data.status === RESPONSE_STATUS.OK) {
        this.$auth.setUserToken(response.data.access_token)
        this.$router.push('/')
      } else if (response.data.status === RESPONSE_STATUS.USER_IS_NOT_VERIFIED) {
        this.$router.push(`/auth/verify/${response.data.id}`)
      }
    },
    onError(response) {
      if (response.status === 401) {
        this.errors = {
          username: response.data.detail,
        }
      }
    },
  },
}
</script>
