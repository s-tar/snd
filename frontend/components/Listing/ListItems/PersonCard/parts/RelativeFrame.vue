<template>
  <div class="person-card__relative-frame">
    <div>
      <div class="person-card__relative-frame-photo">
        <i class="fa-solid fa-user"></i>
      </div>
    </div>
    <div class="person-card__relative-frame-info">
      <div class="person-card__relative-frame-name">{{ name }}</div>
      <InfoFrame>
        <Field name="Родство" :value="relationship" />
        <Field name="Дата рождения" :value="birthday" />
        <Field name="Телефон" :value="phonesString" />
        <AddressField name="Адрес" :value="address" />
        <div v-if="social">
          <SocialField v-for="(link, name) in social" :key="name" :name="name" :value="link" />
        </div>
      </InfoFrame>
    </div>
  </div>
</template>

<script>
import InfoFrame from './InfoFrame'
import Field from './Field'
import AddressField from './AddressField'

export default {
  components: {
    AddressField,
    InfoFrame,
    Field,
  },
  computed: {
    phonesString() {
      return this.phones ? '+' + this.phones.join(', +') : null
    },
  },
  props: {
    name: { type: String, required: true },
    relationship: { type: String, required: true },
    birthday: { type: String, default: null },
    address: { type: String, default: null },
    phones: { type: Array[String], default: null },
    social: { type: Object, default: null },
  },
}
</script>
