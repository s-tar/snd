<template>
  <div></div>
</template>

<script>
export default {
  layout: () => 'simple',
  async created() {
    await this.$auth.logout()
    this.$router.push('/')
  },
}
</script>
