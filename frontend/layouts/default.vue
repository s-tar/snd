<template>
  <div class="page">
    <Header />
    <div class="container container--centered">
      <main class="main-content">
        <Nuxt />
      </main>
    </div>
    <Modal />
  </div>
</template>

<script>
import Modal from '~/components/Modal'
import Header from '~/components/Header'

export default {
  components: {
    Header,
    Modal,
  },
  computed: {
    isAuth() {
      return !!this.$auth.user
    },
  },
}
</script>
