<template>
  <div>
    <Header style="position: relative; z-index: 1000"/>
    <div class="modal">
      <div class="modal__content"><Nuxt /></div>
    </div>
  </div>
</template>
<script>
import Header from '~/components/Header'

export default {
  components: {
    Header,
  },
}
</script>
