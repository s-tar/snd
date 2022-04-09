<template>
  <ul v-if="items.length" class="list">
    <li
      v-for="item in items"
      :key="item.id"
      :class="{
        'list__item': true,
        'list__item--card': true,
        'list__item--inactive': !item.active,
      }"
      @click="item.click"
    >
      <div v-if="item.icon" class="list__item-icon">
        <div class="list__item-badges">
          <i v-for="(badge, index) in item.badges" :key="index" :class="{ 'list__item-badge': true, [badge.icon]: true }"></i>
        </div>
        <i :class="item.icon"></i>
      </div>
      <div class="list__item-info">
        <div class="list__item-title">{{ item.title }}</div>
        <div class="list__item-description">{{ shortDescription(item.description) }}</div>
      </div>
      <div class="list__item-actions">
        <button
          v-for="(button, index) in item.actions"
          :key="index"
          :class="{
            'list__item-button': true,
            [`list__item-button--${button.type}`]: !!button.type,
          }"
          @click.stop="() => actionButtonClick(item.id, button)"
        >
          <i :class="button.icon"></i>
        </button>
      </div>
    </li>
  </ul>
</template>

<script>
export default {
  props: {
    items: { type: Array, required: true },
    getDeleteUrl: { type: Function, required: true },
  },
  methods: {
    async actionButtonClick(id, button) {
      if (button.confirmation) {
        this.$nuxt.$emit('modal-open', {
          title: button.confirmation.title,
          body: button.confirmation.text,
          buttons: [
            { caption: 'Yes', click: () => button.confirmation.action(id), type: 'danger' },
            { caption: 'No', click: () => this.$nuxt.$emit('modal-close'), type: 'info' },
          ],
        })
      } else {
        await button.action(id)
      }
    },
    shortDescription(description) {
      const descriptionLines = description ? description.split('\n') : []
      return descriptionLines[0] + (descriptionLines.length > 1 ? '...' : '')
    },
  },
}
</script>
