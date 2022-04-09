<template>
  <div class="card card--elastic">
    <div class="card__body">
      <AsyncForm
        v-slot="form"
        :action="code ?'/project/' + code : '/project/new'"
        :method="code ? 'put' : 'post'"
        class="form"
        json
        :on-success="onSuccess"
      >
        <div class="form__row">
          <InputField
            id="code"
            type="text"
            name="code"
            label="Code"
            :value="code"
            :readonly="!!code"
          />
        </div>
        <div class="form__row">
          <InputField id="name" type="text" name="name" label="Name" :value="name" />
        </div>
        <div class="form__row">
          <TextAreaField id="description" name="description" :value="description" label="Description" />
        </div>
        <div class="form__row form__row--align-right">
          <nuxt-link to="/" class="button button--danger">Cancel</nuxt-link>
          <Submit type="submit" class="button button--success" :processing="form.processing">{{ code ? 'Save' : 'Create' }}</Submit>
        </div>
      </AsyncForm>
    </div>
  </div>
</template>

<script>
import AsyncForm from '~/components/AsyncForm'
import InputField from '~/components/AsyncForm/fields/Input'
import TextAreaField from '~/components/AsyncForm/fields/Textarea'
import Submit from '~/components/AsyncForm/fields/Submit'

export default {
  name: 'ProjectForm',
  components: {
    InputField,
    TextAreaField,
    AsyncForm,
    Submit,
  },
  props: {
    code: { type: String, default: '' },
    name: { type: String, default: '' },
    description: { type: String, default: '' },
  },
  methods: {
    onSuccess() {
      this.$router.push('/')
    },
  },
}
</script>
