<template>
  <div class="card card--elastic">
    <div class="card__body">
      <AsyncForm
        v-slot="form"
        :action="`/project/${projectCode}/category/${categoryCode}/pack/${packId}/copy`"
        method="post"
        class="form"
        json
        :on-success="onSuccess"
      >
        <div class="form__row">
          <SelectField id="category_code" name="category_code" :value="categoryCode" @change="onCategoryChange" label="Category">
            <option v-for="category in categories" :key="category.code" :value="category.code">{{ category.name }}</option>
          </SelectField>
        </div>
        <div class="form__row">
          <TextAreaField id="description" name="description" :value="description" label="Description" />
        </div>
        <div class="form__row">
          <CheckboxField id="active" name="active" :value="active" label="Active" />
        </div>
        <div class="form__row form__row--align-right">
          <nuxt-link :to="`/project/${projectCode}/category/${categoryCode}`" class="button button--danger">Cancel</nuxt-link>
          <Submit type="submit" class="button button--success" :processing="form.processing">Copy</Submit>
        </div>
      </AsyncForm>
    </div>
  </div>
</template>

<script>
import AsyncForm from '~/components/AsyncForm'
import SelectField from '~/components/AsyncForm/fields/Select'
import TextAreaField from '~/components/AsyncForm/fields/Textarea'
import CheckboxField from '~/components/AsyncForm/fields/Checkbox'
import Submit from '~/components/AsyncForm/fields/Submit'

export default {
  name: 'PackCopyForm',
  components: {
    AsyncForm,
    SelectField,
    TextAreaField,
    CheckboxField,
    Submit,
  },
  props: {
    projectCode: { type: String, required: true },
    categoryCode: { type: String, required: true },
    packId: { type: Number, required: true },
    categories: { type: Array, required: true },
    description: { type: String, default: '' },
    active: { type: Boolean, default: true },
  },
  data() {
    return {
      destinationCategory: this.categoryCode,
    }
  },
  methods: {
    onCategoryChange(e) {
      this.destinationCategory = e.target.value
    },
    onSuccess() {
      this.$router.push(`/project/${this.projectCode}/category/${this.destinationCategory}`)
    },
  },
}
</script>
