<template>
  <div class="card card--elastic">
    <div class="card__body">
      <AsyncForm
        v-slot="form"
        action="/persons/save"
        json
        method="post"
        class="form"
        :on-success="onSuccess"
        :process-data="processData"
      >
        <div class="form__row">
          <div class="form__col form__col--compact">
            <div class="form__row">
              <PhotoField
                id="photo"
                name="photo"
                label="Фото"
                :value="photo"
                @change="onPhotoChange"
              />
            </div>
          </div>
          <div class="form__col">
            <div class="form__row">
              <div class="form__col">
                <InputField id="last_name" type="text" name="last_name" label="Фамилия" :value="person.last_name" />
              </div>
              <div class="form__col">
                <InputField id="first_name" type="text" name="first_name" label="Имя" :value="person.first_name" />
              </div>
              <div class="form__col">
                <InputField id="middle_name" type="text" name="middle_name" label="Отчество" :value="person.middle_name" />
              </div>
            </div>
            <div class="form__row">
              <div class="form__col">
                <SelectField id="type" name="type" :value="personType" @change="e => personType = parseInt(e.target.value)">
                  <option v-for="(type, typeId) of TYPES" :key="typeId" :value="typeId">{{ type }}</option>
                </SelectField>
              </div>
              <div class="form__col">
                <SelectField id="status" name="status" :value="person.status || 1" label="Статус">
                  <option v-for="(status, statusId) of STATUS" :key="statusId" :value="statusId">{{ status }}</option>
                </SelectField>
              </div>
            </div>
          </div>
        </div>
        <InfoFrame title="Личная информация">
          <div class="form__row">
            <div class="form__col form__col--compact">
              <DatetimeField id="birthday" type="date" name="birthday" label="День рождения" :value="person.birthday" />
            </div>
            <div class="form__col">
              <InputField id="city_of_birth" type="text" name="city_of_birth" label="Место рождения" :value="person.city_of_birth" />
            </div>
          </div>
          <div class="form__row">
            <div class="form__col form__col--compact">
              <InputField
                id="passport[number]"
                type="text"
                name="passport[number]"
                label="Номер паспорта"
                :value="passport.number"
                :style="{ minWidth: '130px' }"
              />
            </div>
            <div class="form__col form__col--compact">
              <DatetimeField
                id="passport[date]"
                type="date"
                name="passport[date]"
                label="Дата выдачи"
                :value="passport.date"
                :style="{ minWidth: '100px' }"
              />
            </div>
            <div class="form__col">
              <InputField id="passport.authority" type="text" name="passport.authority" label="Кем выдан" :value="passport.authority"  />
            </div>
          </div>
          <div class="form__row">
            <div class="form__col">
              <InputField
                id="identification_number"
                type="text"
                name="identification_number"
                label="ИНН"
                :value="person.identification_number"
                @keydown="isNumber"
              />
            </div>
          </div>
          <div class="form__row">
            <div class="form__col">
              <InputField
                id="insurance_number"
                type="text"
                name="insurance_number"
                label="СНИЛС"
                :value="person.insurance_number"
                @keydown="isNumber"
              />
            </div>
          </div>
          <div v-for="(address, i) in addresses" :key="i" class="form__row">
            <div class="form__col">
              <InputField
                :id="'addresses'+i"
                type="text"
                name="addresses"
                :label="i === 0 ? 'Адрес' : 'Доп. адрес'"
                :value="address"
                @keypress="e => onAddressChange(i, e.target.value)"
              />
            </div>
          </div>
          <div class="form__row">
            <div v-for="(phone, i) in phones" :key="i" class="form__col form__col--compact">
              <InputField
                :id="'phones'+i"
                type="text"
                name="phones"
                :label="i === 0 ? 'Телефон' : 'Доп. телефон'"
                :value="phone"
                @keypress="e => onPhoneChange(i, e.target.value)"
                @keydown="isNumber"
              />
            </div>
          </div>
        </InfoFrame>
        <InfoFrame v-if="personType === 2" title="Служба">
          <div class="form__row">
            <div class="form__col form__col--compact">
              <InputField
                id="military.number"
                type="text"
                name="military.number"
                label="Личный номер"
                :value="military.number"
                :style="{ minWidth: '120px' }"
              />
            </div>
            <div class="form__col form__col--compact">
              <SelectField id="military.rank" name="military.rank" :value="military.rank" label="Звание" :style="{ minWidth: '200px' }">
                <option v-for="(rank, id) of RANKS" :key="id" :value="id">{{ rank }}</option>
              </SelectField>
            </div>
            <div class="form__col">
              <InputField id="military.post" type="text" name="military.post" label="Должность" :value="military.post" />
            </div>
          </div>
          <div class="form__row">
            <div class="form__col form__col--compact">
              <InputField
                id="military.ticket.number"
                type="text"
                name="military.ticket.number"
                label="Номер военного билета"
                :value="militaryTicket.number"
                :style="{ minWidth: '180px' }"
              />
            </div>
            <div class="form__col form__col--compact">
              <DatetimeField
                id="military.ticket.date"
                type="date"
                name="military.ticket.date"
                label="Дата выдачи"
                :value="militaryTicket.date"
                :style="{ minWidth: '100px' }"
              />
            </div>
            <div class="form__col">
              <InputField
                id="military.ticket.authority"
                type="text"
                name="military.ticket.authority"
                label="Кем выдан"
                :value="militaryTicket.authority"
              />
            </div>
          </div>
          <div class="form__row">
            <div class="form__col">
              <AutocompleteField
                id="military.unity"
                name="military.unity."
                label="Воинская часть"
                :items="getUnits"
                :value="military.unity"
              />
            </div>
          </div>
        </InfoFrame>
        <div class="form__row">
          <div class="form__col form__col--align-right">
            <nuxt-link :to="`/`" class="button button--danger">Отмена</nuxt-link>
            <Submit type="submit" class="button button--success" :processing="form.processing">{{ id ? 'Сохранить' : 'Добавить' }}</Submit>
          </div>
        </div>
      </AsyncForm>
    </div>
  </div>
</template>

<script>
import { TYPES } from '~/utils/types'
import { STATUS } from '~/utils/status'
import { RANKS } from '~/utils/ranks'

import AsyncForm from '~/components/AsyncForm'
import InputField from '~/components/AsyncForm/fields/Input'
import Submit from '~/components/AsyncForm/fields/Submit'
import PhotoField from '~/components/AsyncForm/fields/PhotoField'
import SelectField from '~/components/AsyncForm/fields/Select'
import DatetimeField from '~/components/AsyncForm/fields/Datetime'
import AutocompleteField from '~/components/AsyncForm/fields/Autocomplete'
import InfoFrame from '~/components/InfoFrame'

export default {
  name: 'PersonForm',
  components: {
    InfoFrame,
    PhotoField,
    AsyncForm,
    InputField,
    Submit,
    SelectField,
    DatetimeField,
    AutocompleteField,
  },
  props: {
    id: { type: String, default: '' },
    data: { type: Object, default: () => {} },
  },
  computed: {
    military() {
      return this.data.military || {}
    },
    militaryTicket() {
      return this.military.ticket || {}
    },
    passport() {
      return this.data.passport || {}
    },
    photo() {
      const { id, photo } = this.person
      if (!photo) {
        return null
      }
      return photo.startsWith('data:') ? photo : `/public/person/${id}/${photo}`
    },
    phones() {
      if (this.person.phones && this.person.phones.length === 3) {
        return this.person.phones
      }
      return [...(this.person.phones || []), null]
    },
    addresses() {
      if (this.person.address && this.person.address.length === 2) {
        return this.person.address
      }
      return [...(this.person.address || []), null]
    },
  },
  data() {
    return {
      TYPES,
      STATUS,
      RANKS,
      personType: this.data.type || 2,
      person: this.data,
      unitRequestCanceler: null,
    }
  },
  methods: {
    async getUnits(term) {
      if (term.length > 1) {
        term = term.replace(/[,;.]/g, ' ').replace('в/ч', '')
        const items = {}
        if (this.unitRequestCanceler) {
          this.unitRequestCanceler.cancel()
        }
        this.unitRequestCanceler = this.$axios.CancelToken.source()
        const response = await this.$axios.$get(
          '/unit/search',
          { params: { s: term }, cancelToken: this.unitRequestCanceler.token },
        )
        response.items.forEach((unit) => {
          const name = []
          if (unit.number) {
            name.push('в/ч ' + unit.number)
          }
          if (unit.name) {
            name.push(unit.name)
          }
          items[unit.id] = name.join(', ')
        })
        return items
      }
      return {}
    },
    isNumber(e) {
      if (!['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Backspace', 'Delete'].includes(e.key)) {
        e.preventDefault()
        return false
      }
    },
    onPhoneChange(i, value) {
      if (!this.person.phones || this.person.phones.length === 0) {
        this.$set(this.person, 'phones', [value])
      } else {
        this.$set(this.person.phones, i, value)
      }
    },
    onAddressChange(i, value) {
      if (!this.person.address || this.person.address.length === 0) {
        this.$set(this.person, 'address', [value])
      } else {
        this.$set(this.person.address, i, value)
      }
    },
    onPhotoChange(file, coordinates, canvas) {
      this.$set(this.person, 'photo', canvas.toDataURL('image/jpeg'))
    },
    processData(e) {
      const form = new FormData(e.target)
      // form.delete('pack')
      // form.delete('bundles_zip')
      const dataJson = Object.fromEntries(form)
      console.log(dataJson)
      // dataJson.bundles = this.bundles
      //
      // const finalForm = new FormData()
      // finalForm.append('data', JSON.stringify(dataJson))
      // if (this.bundlesZip) {
      //   finalForm.append('bundles_zip', this.bundlesZip)
      // }
      // return finalForm
    },
    onSuccess() {
      this.$router.push(`/project/${this.projectCode}/category/${this.categoryCode}`)
    },
  },
}
</script>
