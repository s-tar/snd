<template>
  <div class="card">
    <div class="card__header">
      <div class="card__title">Account Verification</div>
    </div>
    <div class="card__body">
      <AsyncForm
        v-slot="form"
        json
        action="/user/verify"
        method="post"
        class="form"
        :errors="errors"
        :is-success="isSuccess"
        :on-success="onSuccess"
        :on-error="onError"
      >
        <div class="form__row form__row--direction-column">
          <InputField name="id" :value="id" type="hidden" />
          <div class="form__text">
            <div>Email with verification code was sent to your mail</div>
            <div>Please check and enter code below</div>
          </div>
        </div>
        <div class="form__row">
          <div v-for="(_, index) in numbersCount" :key="index" class="form__col">
            <InputField
              :id="'number'+index"
              :ref="'number'"
              :value="numbers[index]"
              type="text"
              maxlength="1"
              :field-class="{ 'number-verification-field': true }"
              @keydown="isNumber"
              @keypress="(e) => onPress(index, e)"
            />
          </div>
        </div>
        <div class="form__row">
          <div class="form__col form__col--align-stretch">
            <div class="form__text">
              <InputField name="code" :value="code" type="hidden" />
            </div>
            <Submit type="submit" class="button button--success" :processing="form.processing">Verify</Submit>
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
      focused: null,
      numbersCount: 6,
      numbers: [],
      id: this.$route.params.user_id,
    }
  },
  computed: {
    code() {
      return this.numbers.join('')
    },
  },
  methods: {
    onPress(index, e) {
      this.$set(this.numbers, index, e.key)
      if (index < this.numbersCount - 1) {
        setTimeout(() => {
          this.$refs.number[index + 1].$refs.field.focus()
        }, 100)
      }
    },
    isNumber(e) {
      if (!['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Backspace', 'Delete'].includes(e.key)) {
        e.preventDefault()
        return false
      }
    },
    isSuccess(response) {
      return response.data.status !== RESPONSE_STATUS.DATA_VALIDATION_FAILED
    },
    onSuccess(response) {
      if (response.data.status === RESPONSE_STATUS.OK) {
        this.$auth.setUserToken(response.data.access_token)
        this.$router.push('/')
      }
    },
    onError(response) {},
  },
}
</script>
