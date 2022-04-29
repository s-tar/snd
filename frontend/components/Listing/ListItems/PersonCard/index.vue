<template>
  <div
    :class="{
      'person-card': true,
      'person-card--inactive': !item.active,
    }"
  >
    <div class="person-card__header">
      <div class="person-card__photo">
        <div v-if="item.person.status > 1" class="person-card__photo-badge">
          <i v-if="item.person.status === 2" class="fa-solid fa-skull-crossbones" title="Умер"></i>
          <i v-else-if="item.person.status === 3" class="fa-solid fa-handcuffs" title="В плену"></i>
        </div>
        <img v-if="item.person.photo" :src="getPhoto(item.person)" class="person-card__photo-image" alt="" @click="onPhotoClick(item.person)" />
        <div v-else>
          <i v-if="item.person.status === 2" class="fa-solid fa-skull"></i>
          <i v-else-if="item.person.status === 3" class="fa-solid fa-handcuffs"></i>
          <i v-else class="fa-solid fa-user"></i>
        </div>
      </div>
      <div class="person-card__container person-card__title" @click.self="item.click">
        <div v-if="item.person.country" class="person-card__badge person-card__country-flag-badge" @click="item.click">
          <Flag :code="item.person.country" />
        </div>
        <div class="person-card__name" @click="item.click">
          <span v-if="item.person.last_name">{{ item.person.last_name }}</span>
          <span v-if="item.person.first_name">{{ item.person.first_name }}</span>
          <span v-if="item.person.middle_name">{{ item.person.middle_name }}</span>
          <a v-if="canEdit" :href="`/person/${item.person.code}/edit`" class="link person-card__edit-link" @click.stop="">
            (Редактировать)
          </a>
        </div>
        <div v-if="item.person.birthday" class="person-card__birthday">{{ getDate(item.person.birthday) }}р.</div>
      </div>
      <div class="person-card__short-info" @click.self="item.click">
        <div v-if="item.person.military" class="person-card__container" @click="item.click">
          <div>
            <div
              v-if="item.person.military.rank"
              :class="{
                'person-card__badge person-card__rank-badge': true,
                ['rank-' + item.person.military.rank.toLowerCase()]: true
              }"
              :title="getRank(item.person.military.rank)"
            ></div>
            <div v-else class="person-card__badge person-card__rank-badge"></div>
          </div>
          <div>
            <div>
              <span v-if="item.person.military.post">{{ item.person.military.post }}</span>
              <span v-if="item.person.military.rank" class="person-card__short-info-rank">{{ getRank(item.person.military.rank) }}</span>
            </div>
            <div v-if="item.person.military && item.person.military.unitData">{{ item.person.military.unitData.name }}</div>
          </div>
        </div>
        <div v-if="item.person.tags" class="person-card__container person-card__tags">
          <a v-for="tag in item.person.tags" :key="tag" class="link person-card__tag" :href="`/?s=${tag}`">#{{ tag }}</a>
        </div>
      </div>
    </div>
    <div v-if="item.person.showFullInfo" class="person-card__full-info">
      <div class="person-card__frame-row">
        <div v-if="item.person.military" class="person-card__frame-col">
          <InfoFrame title="Служба" type="table">
            <Field name="Личный номер" :value="item.person.military.number" />
            <Field name="Звание" :value="getRank(item.person.military.rank)" />
            <Field name="Должность" :value="item.person.military.post" />
            <MilitaryUnitField name="Воинская часть" :value="item.person.military.unitData || {}" />
            <Field name="Военный билет" :value="Object.values(getDoc(item.person.military.ticket))" />
          </InfoFrame>
        </div>
        <div v-if="Object.keys(personal).length > 0" class="person-card__frame-col">
          <InfoFrame title="Личные данные" type="table">
            <Field name="День рождения" :value="getDate(personal.birthday)" />
            <Field name="Место рождения" :value="personal.city_of_birth" />
            <Field name="Паспорт" :value="Object.values(getDoc(personal.passport))" />
            <Field name="ИНН" :value="personal.identification_number" />
            <Field name="СНИЛС" :value="personal.insurance_number" />
            <Field name="Телефон" :value="personal.phones" />
            <AddressField name="Адрес" :value="personal.addresses" />
          </InfoFrame>
          <InfoFrame v-if="personal.social">
            <SocialField v-for="(link, name) in personal.social" :key="name" :name="name" :value="link" />
          </InfoFrame>
        </div>
      </div>
      <div v-if="item.person.extra" class="person-card__frame-row">
        <div class="person-card__frame-col">
          <InfoFrame title="Дополнительная информация">
            <div class="person-card__extra">
              <div v-for="(line, i) in item.person.extra.split('\n')" :key="i">{{ line || '&nbsp;' }}</div>
            </div>
          </InfoFrame>
        </div>
      </div>
      <div v-if="item.person.relatives" class="person-card__frame-row">
        <div class="person-card__frame-col">
          <InfoFrame type="table" title="Родственики">
            <RelativeFrame
              v-for="(relative, i) in item.person.relatives"
              :key="i"
              :name="relative.name"
              :relationship="getRelationship(relative.relationship)"
              :birthday="relative.birthday ? getDate(relative.birthday) : null"
              :address="relative.address"
              :phones="relative.phones"
              :social="relative.social"
            />
          </InfoFrame>
        </div>
      </div>
      <div v-if="item.person.sources" class="person-card__frame-row">
        <InfoFrame type="table">
          <Field name="Источник" :value="item.person.sources" />
        </InfoFrame>
      </div>
    </div>
  </div>
</template>

<script>
import InfoFrame from './parts/InfoFrame'
import Field from './parts/Field'
import AddressField from './parts/AddressField'
import MilitaryUnitField from './parts/MilitaryUnitField'
import SocialField from './parts/SocialField'
import RelativeFrame from './parts/RelativeFrame'
import { RANKS } from '~/utils/ranks'
import { RELATIONSHIP } from '~/utils/relationship'
import { formatDateTime } from '~/utils/datetime'

export default {
  components: {
    InfoFrame,
    Field,
    AddressField,
    MilitaryUnitField,
    SocialField,
    RelativeFrame,
  },
  props: {
    item: { type: Object, required: true },
  },
  computed: {
    canEdit() {
      return this.$auth.user && this.$auth.user.role > 1
    },
    personal() {
      const personal = {
        birthday: this.item.person.birthday,
        city_of_birth: this.item.person.city_of_birth,
        passport: this.item.person.passport,
        identification_number: this.item.identification_number,
        insurance_number: this.item.person.insurance_number,
        phones: this.phones,
        addresses: this.item.person.addresses,
        social: this.item.person.social,
      }
      for (const [key, value] of Object.entries(personal)) {
        if (
          value == null ||
          value === '' ||
          (Array.isArray(value) && value.length === 0) ||
          (typeof value === 'object' && Object.keys(value).length === 0)
        ) {
          delete personal[key]
        }
      }
      return personal
    },
    phones() {
      return (this.item.person.phones || []).map(phone => '+' + phone)
    },
  },
  methods: {
    getDoc(doc) {
      if (!doc) {
        return {}
      }
      return {
        number: doc.number,
        date: doc.date ? this.getDate(doc.date) : null,
        authority: doc.authority,
      }
    },
    getPhoto(person, fullScale = false) {
      let photoName = person.photo
      if (fullScale) {
        const [name, hex,, ext] = photoName.split('.')
        photoName = `${name}.${hex}.${ext}`
      }
      return `/public/person/${person.id}/${photoName}`
    },
    getRank(code) {
      return RANKS[code] || ''
    },
    getRelationship(code) {
      code = Number.isInteger(code) ? code : parseInt(code)
      return RELATIONSHIP[code] || ''
    },
    getDate(date) {
      if (date == null) {
        return null
      }
      return formatDateTime(date, { year: 'numeric', month: 'long', day: 'numeric' })
    },
    onPhotoClick(person) {
      this.$viewerApi({
        options: { toolbar: false, title: false, movable: false },
        images: [this.getPhoto(person, true)],
      })
    },
  },
}
</script>
