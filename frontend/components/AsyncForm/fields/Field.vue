<script>
export default {
  props: {
    id: { type: String, default: null },
    name: { type: String, default: null },
    value: { type: [String, Number], default: '' },
    label: { type: String, default: null },
    type: { type: String, default: null },
    readonly: { type: Boolean, default: false },
    fieldClass: { type: Object, default: () => {} },
    keepChanged: { type: Boolean, default: true },
  },
  data() {
    return {
      error: null,
    }
  },
  mounted() {
    this.$on('errors', (errors) => {
      this.error = errors[this.name]
    })
  },
}
</script>
