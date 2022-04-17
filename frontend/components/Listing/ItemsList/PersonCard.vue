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
          <img :src="getPhoto(item.person)" class="person-card__photo-image" alt=""/>
          <i v-if="!item.person.photo" :class="item.icon"></i>
        </div>
        <div class="person-card__short-info" @click="item.click">
          <div class="person-card__container person-card__title">
            <div v-if="item.person.country" class="person-card__badge person-card__country-flag-badge">
              <Flag :code="item.person.country" />
            </div>
            <div class="person-card__name">{{ item.title }}</div>
            <div v-if="item.person.birthday">{{ getDate(item.person.birthday) }}</div>
          </div>
          <div v-if="item.person.military" class="person-card__container">
            <div
              v-if="item.person.military.rank"
              :class="'person-card__badge person-card__rank-badge ' + 'rank-' + item.person.military.rank.toLowerCase()"
              :title="getRank(item.person.military.rank)"
            ></div>
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
              <div class="table">
                <div v-if="item.person.military.number" class="table__row">
                  <div class="table__cell person-card__frame-field-name">Личный номер:</div>
                  <div class="table__cell person-card__frame-field-value">{{ item.person.military.number }}</div>
                </div>
                <div v-if="item.person.military.rank" class="table__row">
                  <div class="table__cell person-card__frame-field-name">Звание:</div>
                  <div class="table__cell person-card__frame-field-value">{{ getRank(item.person.military.rank) }}</div>
                </div>
                <div v-if="item.person.military.post" class="table__row">
                  <div class="table__cell person-card__frame-field-name">Должность:</div>
                  <div class="table__cell person-card__frame-field-value">{{ item.person.military.post }}</div>
                </div>
                <div v-if="item.squad" class="table__row">
                  <div class="table__cell person-card__frame-field-name">Подразделение:</div>
                  <div class="table__cell person-card__frame-field-value">
                    <span v-if="item.squad.name">{{ item.squad.name }}<br /></span>
                    <span v-if="item.squad.unit_number">в\ч {{ item.squad.unit_number }}<br /></span>
                    <span v-if="item.squad.address">{{ item.squad.address }}<br /></span>
                  </div>
                </div>
                <div v-if="item.person.military.ticket" class="table__row">
                  <div class="table__cell person-card__frame-field-name">Военный билет:</div>
                  <div class="table__cell person-card__frame-field-value">
                    <span v-if="item.person.military.ticket.number">{{ item.person.military.ticket.number }}<br /></span>
                    <span v-if="item.person.military.ticket.date">в\ч {{ getDate(item.person.military.ticket.date) }}<br /></span>
                    <span v-if="item.person.military.ticket.authority">{{ item.person.military.ticket.authority }}<br /></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="person-card__frame">
            <div class="person-card__frame-title">Личные данные</div>
            <div class="person-card__frame-body">
              <div class="table">
                <div v-if="item.person.birthday" class="table__row">
                  <div class="table__cell person-card__frame-field-name">День рождения:</div>
                  <div class="table__cell person-card__frame-field-value">{{ getDate(item.person.birthday) }}</div>
                </div>
                <div v-if="item.person.passport" class="table__row">
                  <div class="table__cell person-card__frame-field-name">Паспорт:</div>
                  <div class="table__cell person-card__frame-field-value">
                    <span v-if="item.person.passport.number">{{ item.person.passport.number }}<br /></span>
                    <span v-if="item.person.passport.date">в\ч {{ getDate(item.person.passport.date) }}<br /></span>
                    <span v-if="item.person.passport.authority">{{ item.person.passport.authority }}<br /></span>
                  </div>
                </div>
                <div v-if="item.person.identification_number" class="table__row">
                  <div class="table__cell person-card__frame-field-name">ИНН:</div>
                  <div class="table__cell person-card__frame-field-value">{{ item.person.identification_number }}</div>
                </div>
                <div v-if="item.person.insurance_number" class="table__row">
                  <div class="table__cell person-card__frame-field-name">СНИЛС:</div>
                  <div class="table__cell person-card__frame-field-value">{{ item.person.insurance_number }}</div>
                </div>
                <div v-if="item.person.phones && item.person.phones.length" class="table__row">
                  <div class="table__cell person-card__frame-field-name">Телефон:</div>
                  <div v-for="(phone, i) in item.person.phones" :key="i" class="table__cell person-card__frame-field-value">
                    +{{ phone }}
                  </div>
                </div>
                <div v-if="item.person.address" class="table__row">
                  <div class="table__cell person-card__frame-field-name">Адрес:</div>
                  <div class="table__cell person-card__frame-field-value">{{ item.person.address }}</div>
                </div>
              </div>
              <div v-if="item.person.social" class="table">
                <div v-if="item.person.social.ok" class="table__row">
                  <div class="table__cell person-card__frame-field-name"><i class="fa-brands fa-odnoklassniki"></i></div>
                  <div class="table__cell person-card__frame-field-value">
                    <a :href="item.person.social.ok" target="_blank" class="link">{{ item.person.social.ok }}</a>
                  </div>
                </div>
                <div v-if="item.person.social.vk" class="table__row">
                  <div class="table__cell person-card__frame-field-name"><i class="fa-brands fa-vk"></i></div>
                  <div class="table__cell person-card__frame-field-value">
                    <a :href="item.person.social.vk" target="_blank" class="link">{{ item.person.social.vk }}</a>
                  </div>
                </div>
                <div v-if="item.person.social.fb" class="table__row">
                  <div class="table__cell person-card__frame-field-name"><i class="fa-brands fa-facebook"></i></div>
                  <div class="table__cell person-card__frame-field-value">
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
    getPhoto(person) {
      return `/public/person/${person.id}/${person.photo}`
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
  },
}
</script>
