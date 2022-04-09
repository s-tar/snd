<template>
  <div class="page">
    <header class="header">
      <div class="container container--separated container--centered">
        <div class="header__title">
          <a class="header__logo" href="/">Seek<small>&</small>Destroy</a>
        </div>
        <Profile />
      </div>
    </header>
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

export default {
  components: {
    Modal,
  },
}
</script>
