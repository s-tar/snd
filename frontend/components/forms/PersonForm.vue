<template>
  <div class="card card--elastic">
    <div class="card__body">
      <AsyncForm
        v-slot="form"
        ref="form"
        :action="action"
        json
        method="post"
        class="form"
        :process-errors="processErrors"
        :is-success="isSuccess"
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
                @update="onUpdate"
              />
            </div>
          </div>
          <div class="form__col">
            <div class="form__row">
              <div class="form__col">
                <InputField
                  id="last_name"
                  type="text"
                  name="last_name"
                  label="Фамилия"
                  :value="person.last_name"
                  @update="onUpdate"
                />
              </div>
              <div class="form__col">
                <InputField
                  id="first_name"
                  type="text"
                  name="first_name"
                  label="Имя"
                  :value="person.first_name"
                  @update="onUpdate"
                />
              </div>
              <div class="form__col">
                <InputField
                  id="middle_name"
                  type="text"
                  name="middle_name"
                  label="Отчество"
                  :value="person.middle_name"
                  @update="onUpdate"
                />
              </div>
            </div>
            <div class="form__row">
              <div class="form__col">
                <SelectField
                  id="type"
                  name="type"
                  :value="personType"
                  @change="e => personType = parseInt(e.target.value)"
                  @update="onUpdate"
                >
                  <option v-for="(type, typeId) of TYPES" :key="typeId" :value="typeId">{{ type }}</option>
                </SelectField>
              </div>
              <div class="form__col">
                <SelectField
                  id="country"
                  name="country"
                  label="Страна"
                  :value="person.country || 'RU'"
                  @update="onUpdate"
                >
                  <option v-for="(country, code) of COUNTRIES" :key="code" :value="code">{{ country }}</option>
                </SelectField>
              </div>
              <div class="form__col">
                <SelectField id="status" name="status" :value="person.status || 1" label="Статус" @update="onUpdate">
                  <option v-for="(status, statusId) of STATUS" :key="statusId" :value="statusId">{{ status }}</option>
                </SelectField>
              </div>
            </div>
          </div>
        </div>
        <div class="info-frame">
          <div class="info-frame__title">Личная информация</div>
          <div class="info-frame__body">
            <div class="form__row">
              <div class="form__col form__col--compact">
                <DatetimeField
                  id="birthday"
                  type="date"
                  name="birthday"
                  label="День рождения"
                  :value="person.birthday"
                  @update="onUpdate"
                />
              </div>
              <div class="form__col">
                <InputField
                  id="city_of_birth"
                  type="text"
                  name="city_of_birth"
                  label="Место рождения"
                  :value="person.city_of_birth"
                  @update="onUpdate"
                />
              </div>
            </div>
            <div class="form__row">
              <div class="form__col form__col--compact">
                <InputField
                  id="passport.number"
                  type="text"
                  name="passport.number"
                  label="Номер паспорта"
                  :value="passport.number"
                  :style="{ minWidth: '130px' }"
                  @update="onUpdate"
                />
              </div>
              <div class="form__col form__col--compact">
                <DatetimeField
                  id="passport.date"
                  type="date"
                  name="passport.date"
                  label="Дата выдачи"
                  :value="passport.date"
                  :style="{ minWidth: '100px' }"
                  @update="onUpdate"
                />
              </div>
              <div class="form__col">
                <InputField
                  id="passport.authority"
                  type="text"
                  name="passport.authority"
                  label="Кем выдан"
                  :value="passport.authority"
                  @update="onUpdate"
                />
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
                  @update="onUpdate"
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
                  @update="onUpdate"
                />
              </div>
            </div>
            <div v-for="(address, i) in addresses" :key="i" class="form__row">
              <div class="form__col">
                <InputField
                  :id="'addresses.'+i"
                  type="text"
                  :name="'addresses.'+i"
                  :label="i === 0 ? 'Адрес' : 'Доп. адрес'"
                  :value="address"
                  :keep-changed="false"
                  @input="e => onMultipleChange(i, 'addresses', e.target.value)"
                  @update="onUpdate"
                />
              </div>
            </div>
            <div class="form__row">
              <div v-for="(phone, i) in phones" :key="i" class="form__col form__col--compact">
                <InputField
                  :id="'phones.'+i"
                  type="text"
                  :name="'phones.'+i"
                  :label="i === 0 ? 'Телефон' : 'Доп. телефон'"
                  :value="phone"
                  :keep-changed="false"
                  @input="e => onMultipleChange(i, 'phones', e.target.value)"
                  @keydown="isNumber"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="info-frame">
          <div class="info-frame__title">Социальные сети</div>
          <div class="info-frame__body">
            <div class="form__row">
              <div class="form__col">
                <InputField
                  id="social.vk"
                  type="text"
                  name="social.vk"
                  label="VKontakte"
                  :value="social.vk"
                  @update="onUpdate"
                />
              </div>
            </div>
            <div class="form__row">
              <div class="form__col">
                <InputField
                  id="social.ok"
                  type="text"
                  name="social.ok"
                  label="Odnokassniki"
                  :value="social.ok"
                  @update="onUpdate"
                />
              </div>
            </div>
            <div class="form__row">
              <div class="form__col">
                <InputField
                  id="social.fb"
                  type="text"
                  name="social.fb"
                  label="Facebook"
                  :value="social.fb"
                  @update="onUpdate"
                />
              </div>
            </div>
          </div>
        </div>
        <div v-if="personType === 2" class="info-frame">
          <div class="info-frame__title">Служба</div>
          <div class="info-frame__body">
            <div class="form__row">
              <div class="form__col form__col--compact">
                <InputField
                  id="military.number"
                  type="text"
                  name="military.number"
                  label="Личный номер"
                  :value="military.number"
                  :style="{ minWidth: '120px' }"
                  @update="onUpdate"
                />
              </div>
              <div class="form__col form__col--compact">
                <SelectField
                  id="military.rank"
                  name="military.rank"
                  :value="military.rank"
                  label="Звание"
                  :style="{ minWidth: '200px' }"
                  @update="onUpdate"
                >
                  <option v-for="(rank, key) of RANKS" :key="key" :value="key">{{ rank }}</option>
                </SelectField>
              </div>
              <div class="form__col">
                <InputField
                  id="military.post"
                  type="text"
                  name="military.post"
                  label="Должность"
                  :value="military.post"
                  @update="onUpdate"
                />
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
                  @update="onUpdate"
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
                  @update="onUpdate"
                />
              </div>
              <div class="form__col">
                <InputField
                  id="military.ticket.authority"
                  type="text"
                  name="military.ticket.authority"
                  label="Кем выдан"
                  :value="militaryTicket.authority"
                  @update="onUpdate"
                />
              </div>
            </div>
            <div class="form__row">
              <div class="form__col">
                <AutocompleteField
                  id="military.unit"
                  name="military.unit"
                  label="Воинская часть"
                  :items="getUnits"
                  :value="military.unit ? military.unit.id : null"
                  :term="militaryUnitName"
                  @update="onUpdate"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="info-frame">
          <div class="info-frame__title">Дополнительная информация</div>
          <div class="info-frame__body">
            <div class="form__row">
              <div class="form__col">
                <TextareaField
                  id="extra"
                  name="extra"
                  :value="person.extra"
                  @update="onUpdate"
                />
              </div>
            </div>
            <div v-for="(source, i) in sources" :key="i" class="form__row">
              <div class="form__col">
                <InputField
                  :id="'sources.'+i"
                  type="text"
                  :name="'sources.'+i"
                  :label="i === 0 ? 'Источник' : 'Доп. Источник'"
                  :value="source"
                  :keep-changed="false"
                  @input="e => onMultipleChange(i, 'sources', e.target.value)"
                />
              </div>
            </div>
            <div class="form__row">
              <div v-for="(tag, i) in tags" :key="i" class="form__col form__col--compact">
                <InputField
                  :id="'tags.'+i"
                  type="text"
                  :name="'tags.'+i"
                  label="Тэг"
                  :value="tag"
                  :keep-changed="false"
                  @input="e => onMultipleChange(i, 'tags', e.target.value)"
                />
              </div>
            </div>
          </div>
        </div>
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
import { COUNTRIES } from '~/utils/countries'
import { RESPONSE_STATUS } from '~/utils/response_status'
import { updateByPath } from '~/utils/object'

import AsyncForm from '~/components/AsyncForm'
import InputField from '~/components/AsyncForm/fields/Input'
import Submit from '~/components/AsyncForm/fields/Submit'
import PhotoField from '~/components/AsyncForm/fields/PhotoField'
import SelectField from '~/components/AsyncForm/fields/Select'
import DatetimeField from '~/components/AsyncForm/fields/Datetime'
import AutocompleteField from '~/components/AsyncForm/fields/Autocomplete'
import TextareaField from '~/components/AsyncForm/fields/Textarea'

export default {
  name: 'PersonForm',
  components: {
    TextareaField,
    PhotoField,
    AsyncForm,
    InputField,
    Submit,
    SelectField,
    DatetimeField,
    AutocompleteField,
  },
  props: {
    action: { type: String, required: true },
    id: { type: String, default: '' },
    data: { type: Object, default: () => {} },
  },
  data() {
    return {
      TYPES,
      STATUS,
      RANKS,
      COUNTRIES,
      personType: this.data.type || 2,
      person: this.data,
      unitRequestCanceler: null,
      updatedData: {},
      updatedFiles: {},
    }
  },
  computed: {
    social() {
      return this.data.social || {}
    },
    military() {
      return this.data.military || {}
    },
    militaryTicket() {
      return this.military.ticket || {}
    },
    militaryUnitName() {
      if (this.military.unit) {
        return this.getUnitName(this.military.unit)
      }
      return ''
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
      return [...(this.person.phones || []), null].slice(0, 3)
    },
    addresses() {
      return [...(this.person.addresses || []), null].slice(0, 2)
    },
    sources() {
      return [...(this.person.sources || []), null]
    },
    tags() {
      return [...(this.person.tags || []), null]
    },
  },
  mounted() {
    if (this.data.id) {
      return
    }
    for (const [name, value] of Object.entries(Object.fromEntries(new FormData(this.$refs.form.$el)))) {
      if (value && !(value instanceof File)) {
        updateByPath(this.updatedData, name, value)
      }
    }
  },
  methods: {
    getUnitName(unit) {
      const name = []
      if (unit.number) {
        name.push('в/ч ' + unit.number)
      }
      if (unit.name) {
        name.push(unit.name)
      }
      return name.join(', ')
    },
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
          items[unit.id] = this.getUnitName(unit)
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
    onMultipleChange(i, name, value) {
      const values = this.person[name] ? this.person[name] : []
      if (!(name in this.updatedData)) {
        this.updatedData[name] = new Array(values.length)
      }

      if (!value) {
        this.$delete(this.person[name], i)
        const size = this.updatedData[name].length
        let newArray = this.updatedData[name].slice(0, i).concat(values.slice(i))
        newArray = newArray.concat(new Array(size - newArray.length).fill(''))
        this.updatedData[name] = newArray
      } else if (values.length === 0) {
        this.$set(this.person, name, [value])
        this.updatedData[name].push(value)
      } else {
        this.$set(this.person[name], i, value)
        this.updatedData[name][i] = value
      }
    },
    onPhotoChange(file, coordinates, canvas) {
      this.$set(this.person, 'photo', canvas.toDataURL('image/jpeg'))
    },
    onUpdate(name, value, file) {
      updateByPath(this.updatedData, name, value)
      if (file) {
        this.updatedFiles[name] = file
      }
    },
    processData() {
      const form = new FormData()
      this.updatedData.id = this.data.id
      form.append('data', JSON.stringify(this.updatedData))
      for (const [name, file] of Object.entries(this.updatedFiles)) {
        form.append(name, file)
      }
      return form
    },
    isSuccess(response) {
      return response.data.status !== RESPONSE_STATUS.DATA_VALIDATION_FAILED
    },
    onSuccess(response) {
      this.$router.push(`/person/${response.data.code}`)
    },
    processErrors(response, showErrors) {
      const errors = {}
      response.data.detail.forEach((error) => {
        errors[error.loc.slice(2).join('.')] = error.msg.charAt(0).toUpperCase() + error.msg.slice(1)
      })
      return errors
    },
  },
}
</script>
