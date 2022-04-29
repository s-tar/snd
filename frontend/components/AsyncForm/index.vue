<template>
  <form @submit.prevent="submit"><slot :processing="processing"></slot></form>
</template>

<script>
export default {
  name: 'AsyncForm',
  props: {
    action: { type: String, default: '' },
    method: { type: String, default: 'POST' },
    processErrors: { type: Function, default: null },
    processData: { type: Function, default: null },
    isSuccess: { type: Function, default: null },
    onSuccess: { type: Function, default: null },
    onError: { type: Function, default: null },
    errors: { type: Object, default: null },
    json: { type: Boolean, default: false },
  },
  data() {
    return {
      errors_: this.errors || {},
      files: {},
      processing: false,
    }
  },
  watch: {
    errors(errors) {
      this.updateErrors(errors)
    },
    errors_(errors) {
      this.updateErrors(errors)
    },
  },
  methods: {
    updateErrors(errors) {
      this.$children.forEach((child) => {
        child.$emit('errors', errors)
      })
    },
    processErrors_(response, showErrors) {
      this.processing = false
      if (this.processErrors) {
        this.errors_ = this.processErrors(response, showErrors)
      } else if (showErrors) {
        const errors = {}
        response.data.detail.forEach((error) => {
          errors[error.loc[1]] = error.msg.charAt(0).toUpperCase() + error.msg.slice(1)
        })
        this.errors_ = errors
      }

      if (this.onError) {
        this.onError(response)
      }
    },
    submit(e) {
      if (this.processing) { return false }

      this.processing = true
      this.updateErrors({})
      let data = null
      let headers = null
      if (this.processData) {
        data = this.processData(e)
      } else {
        data = new FormData(e.target)
        if (this.json) {
          headers = {
            'Content-Type': 'application/json',
          }
          data = JSON.stringify(Object.fromEntries(data))
        }
      }
      if (!data) {
        this.processing = false
        return false
      }

      this.$axios({
        headers,
        method: this.method,
        url: this.action,
        data,
      })
        .then((response) => {
          if (this.isSuccess && !this.isSuccess(response)) {
            return this.processErrors_(response, true)
          } else if (this.onSuccess) {
            this.onSuccess(response)
          }
        })
        .catch((error) => {
          this.processErrors_(error.response, error.response.status === 422)
        })
    },
  },
}
</script>
