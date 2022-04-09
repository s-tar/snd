<template>
  <div v-if="visible" class="modal">
    <div class="modal__background" @click.stop="close"></div>
    <div class="modal__content">
      <div class="card">
        <div v-if="title" class="card__header">
          <div class="card__title">{{ title }}</div>
        </div>
        <div class="card__body">
          <div class="card__content">
            {{ body }}
          </div>
          <div v-if="buttons" class="card__content">
            <div class="container container--separated container--centred">
              <button
                v-for="(button, index) in buttons"
                :key="index"
                :class="`button button--${button.type || 'default'}`"
                @click.prevent="button.click"
              >
                {{ button.caption }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Modal',
  data() {
    return {
      title: null,
      body: '',
      buttons: null,
      visible: false,
    }
  },
  created() {
    this.$nuxt.$on('modal-open', this.open)
    this.$nuxt.$on('modal-close', this.close)
  },
  methods: {
    open({ title, body, buttons }) {
      this.title = title
      this.body = body
      this.buttons = buttons
      this.visible = true
    },
    close() {
      this.visible = false
    },
  },
}
</script>
