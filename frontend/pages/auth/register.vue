<template>
  <div class="card registration-form">
    <div class="card__header">
      <div class="card__title">Registration</div>
    </div>
    <div class="card__body">
      <AsyncForm
        v-slot="form"
        action="/users/register"
        method="post"
        class="form"
        json
        :errors="errors"
        :is-success="isSuccess"
        :on-success="onSuccess"
        :on-error="onError"
      >
        <div class="form__row">
          <InputField id="name" type="text" name="name" label="Name" />
        </div>
        <div class="form__row">
          <InputField id="email" type="email" name="email" label="Email" />
        </div>
        <div class="form__row">
          <InputField id="password" type="password" name="password" label="Password" />
        </div>
        <div class="form__row">
          <InputField id="repassword" type="password" name="repassword" label="Confirm Password" />
        </div>
        <div class="form__row form__row--valign-center form__row--align-stretch">
          <a href="/auth/login" class="link">Login</a>
          <Submit type="submit" class="button button--success" :processing="form.processing">Register</Submit>
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
        this.$router.push(`/auth/verify/${response.data.id}`)
      } else if (response.data.status === RESPONSE_STATUS.DATA_VALIDATION_FAILED) {
        this.errors = response.error
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
