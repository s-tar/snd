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
        <Field name="" :value="relationship" />
        <Field name="Дата рождения" :value="birthday" />
        <Field name="Телефон" :value="phonesString" />
        <AddressField name="Адрес" :value="address" />
        <div v-if="social">
          <SocialField v-for="(link, snName) in social" :key="snName" :name="snName" :value="link" />
        </div>
      </InfoFrame>
    </div>
  </div>
</template>

<script>
import InfoFrame from './InfoFrame'
import Field from './Field'
import SocialField from './SocialField'
import AddressField from './AddressField'

export default {
  components: {
    AddressField,
    InfoFrame,
    Field,
    SocialField,
  },
  props: {
    name: { type: String, required: true },
    relationship: { type: String, required: true },
    birthday: { type: String, default: null },
    address: { type: String, default: null },
    phones: { type: Array[String], default: null },
    social: { type: Object, default: null },
  },
  computed: {
    phonesString() {
      return this.phones ? '+' + this.phones.join(', +') : null
    },
  },
}
</script>
