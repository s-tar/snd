<template>
  <ul v-if="items.length" class="list">
    <li
      v-for="item in items"
      :key="item.id"
      :class="{
        'person-card': true,
        'person-card--inactive': !item.active,
      }"
    >
      <div class="person-card__header">
        <div class="person-card__photo">
          <img v-if="item.person.photo" :src="getPhoto(item.person)" @click="onPhotoClick(item.person)" class="person-card__photo-image" alt=""/>
          <i v-else :class="item.icon"></i>
        </div>
        <div class="person-card__container person-card__title" @click="item.click">
          <div v-if="item.person.country" class="person-card__badge person-card__country-flag-badge">
            <Flag :code="item.person.country" />
          </div>
          <div class="person-card__name">
            <span v-if="item.person.last_name">{{ item.person.last_name }}</span>
            <span v-if="item.person.first_name">{{ item.person.first_name }}</span>
            <span v-if="item.person.middle_name">{{ item.person.middle_name }}</span>
          </div>
          <div class="person-card__birthday" v-if="item.person.birthday">{{ getDate(item.person.birthday) }}р.</div>
        </div>
        <div class="person-card__short-info" @click="item.click">
          <div v-if="item.person.military" class="person-card__container">
            <div>
              <div
                v-if="item.person.military.rank"
                :class="'person-card__badge person-card__rank-badge ' + 'rank-' + item.person.military.rank.toLowerCase()"
                :title="getRank(item.person.military.rank)"
              ></div>
            </div>
            <div>
              <div>{{ item.person.military.post }} ({{ getRank(item.person.military.rank) }})</div>
              <div v-if="item.squad">{{ item.squad.name }}</div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="item.person.showFullInfo" class="person-card__full-info">
        <div class="person-card__frame-row">
          <div v-if="item.person.military" class="person-card__frame">
            <div class="person-card__frame-title">Служба</div>
            <div class="person-card__frame-body">
              <div class="person-card__frame-fields">
                <div v-if="item.person.military.number" class="person-card__frame-field">
                  <div class="person-card__frame-field-name">Личный номер:</div>
                  <div class="person-card__frame-field-value">{{ item.person.military.number }}</div>
                </div>
                <div v-if="item.person.military.rank" class="person-card__frame-field">
                  <div class="person-card__frame-field-name">Звание:</div>
                  <div class="person-card__frame-field-value">{{ getRank(item.person.military.rank) }}</div>
                </div>
                <div v-if="item.person.military.post" class="person-card__frame-field">
                  <div class="person-card__frame-field-name">Должность:</div>
                  <div class="person-card__frame-field-value">{{ item.person.military.post }}</div>
                </div>
                <div v-if="item.squad" class="person-card__frame-field">
                  <div class="person-card__frame-field-name">Подразделение:</div>
                  <div class="person-card__frame-field-value">
                    <span v-if="item.squad.name">{{ item.squad.name }}<br /></span>
                    <span v-if="item.squad.unit_number">в\ч {{ item.squad.unit_number }}<br /></span>
                    <span v-if="item.squad.address">{{ item.squad.address }}<br /></span>
                  </div>
                </div>
                <div v-if="item.person.military.ticket" class="person-card__frame-field">
                  <div class="person-card__frame-field-name">Военный билет:</div>
                  <div class="person-card__frame-field-value">
                    <span v-if="item.person.military.ticket.number">{{ item.person.military.ticket.number }}<br /></span>
                    <span v-if="item.person.military.ticket.date">{{ getDate(item.person.military.ticket.date) }}<br /></span>
                    <span v-if="item.person.military.ticket.authority">{{ item.person.military.ticket.authority }}<br /></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="person-card__frame">
            <div class="person-card__frame-title">Личные данные</div>
            <div class="person-card__frame-body">
              <div class="person-card__frame-fields">
                <div v-if="item.person.birthday" class="person-card__frame-field">
                  <div class="person-card__frame-field-name">День рождения:</div>
                  <div class="person-card__frame-field-value">{{ getDate(item.person.birthday) }}</div>
                </div>
                <div v-if="item.person.passport" class="person-card__frame-field">
                  <div class="person-card__frame-field-name">Паспорт:</div>
                  <div class="person-card__frame-field-value">
                    <span v-if="item.person.passport.number">{{ item.person.passport.number }}<br /></span>
                    <span v-if="item.person.passport.date">в\ч {{ getDate(item.person.passport.date) }}<br /></span>
                    <span v-if="item.person.passport.authority">{{ item.person.passport.authority }}<br /></span>
                  </div>
                </div>
                <div v-if="item.person.identification_number" class="person-card__frame-field">
                  <div class="person-card__frame-field-name">ИНН:</div>
                  <div class="person-card__frame-field-value">{{ item.person.identification_number }}</div>
                </div>
                <div v-if="item.person.insurance_number" class="person-card__frame-field">
                  <div class="person-card__frame-field-name">СНИЛС:</div>
                  <div class="person-card__frame-field-value">{{ item.person.insurance_number }}</div>
                </div>
                <div v-if="item.person.phones && item.person.phones.length" class="person-card__frame-field">
                  <div class="person-card__frame-field-name">Телефон:</div>
                  <div v-for="(phone, i) in item.person.phones" :key="i" class="person-card__frame-field-value">
                    +{{ phone }}
                  </div>
                </div>
                <div v-if="item.person.addresses" class="person-card__frame-field">
                  <div class="person-card__frame-field-name">Адреса:</div>
                  <div class="person-card__frame-field-value">
                      <span v-for="(address, i) in item.person.addresses" :key="i">
                        <i class="fa-solid fa-location-dot"></i> {{ address }}<br />
                      </span>
                  </div>
                </div>
              </div>
              <div v-if="item.person.social" class="person-card__frame-fields">
                <div v-if="item.person.social.ok" class="person-card__frame-field">
                  <div class="person-card__frame-field-name"><i class="fa-brands fa-odnoklassniki"></i></div>
                  <div class="person-card__frame-field-value">
                    <a :href="item.person.social.ok" target="_blank" class="link">{{ item.person.social.ok }}</a>
                  </div>
                </div>
                <div v-if="item.person.social.vk" class="person-card__frame-field">
                  <div class="person-card__frame-field-name"><i class="fa-brands fa-vk"></i></div>
                  <div class="person-card__frame-field-value">
                    <a :href="item.person.social.vk" target="_blank" class="link">{{ item.person.social.vk }}</a>
                  </div>
                </div>
                <div v-if="item.person.social.fb" class="person-card__frame-field">
                  <div class="person-card__frame-field-name"><i class="fa-brands fa-facebook"></i></div>
                  <div class="person-card__frame-field-value">
                    <a :href="item.person.social.fb" target="_blank" class="link">{{ item.person.social.fb }}</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="item.person.extra" class="person-card__frame-row">
          <div class="person-card__frame">
            <div class="person-card__frame-title">Дополнительная информация</div>
            <div class="person-card__frame-body">{{ item.person.extra }}</div>
          </div>
        </div>
      </div>
    </li>
  </ul>
</template>

<script>
import { RANKS } from '~/utils/ranks'
import { formatDateTime } from '~/utils/datetime'

export default {
  components: {
  },
  props: {
    items: { type: Array, required: true },
    getDeleteUrl: { type: Function, required: true },
  },
  methods: {
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
    getDate(date) {
      return formatDateTime(date, { year: 'numeric', month: 'long', day: 'numeric' })
    },
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
    onPhotoClick(person) {
      this.$viewerApi({
        options: { toolbar: false, title: false, movable: false },
        images: [this.getPhoto(person, true)],
      })
    },
  },
}
</script>
