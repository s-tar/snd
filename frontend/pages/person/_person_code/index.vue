<script>
import Listing from '~/components/Listing'
import PersonCard from '~/components/Listing/ListItems/PersonCard'
import { RESPONSE_STATUS } from '~/utils/response_status'
import { RANKS } from '~/utils/ranks'
import { formatDateTime } from '~/utils/datetime'

export default {
  extends: Listing,
  auth: false,
  data() {
    return {
      person: {},
      unit: {},
    }
  },
  head() {
    const meta = []
    const description = this.getMetaDescription()
    meta.push({ hid: 'og-url', property: 'og:url', content: this.$route.path })
    meta.push({ hid: 'og-description', property: 'og:description', description })
    meta.push({ hid: 'description', property: 'description', description })
    if (this.person.photo) {
      meta.push({
        hid: 'og-image', property: 'og:image', content: `/public/person/${this.person.id}/${this.person.photo}`,
      })
    }
    return { meta }
  },
  computed: {
    withSearch() { return true },
    mainTitle() {
      return ''
    },
    itemsListComponent() {
      return PersonCard
    },
    items() {
      return [{
        id: this.person.code,
        icon: 'fa-solid fa-user',
        person: this.person,
        active: true,
        click: () => {},
        isPersonPage: true,
        actions: [],
      }]
    },
  },
  methods: {
    async init() {
      const res = await this.loadPerson()
      if (res.status !== RESPONSE_STATUS.OK || !res.person) {
        return this.$nuxt.error({ statusCode: 404, message: 'Страница не найдена' })
      }
      this.person = res.person
      if (this.person.military && this.person.military.unit) {
        this.person.military.unitData = await this.loadMilitaryUnit(this.person.military.unit)
      }
      this.person.showFullInfo = true
      this.loading = false
    },
    async loadMilitaryUnit(id) {
      const res = await this.$axios.$get(
        '/unit/get',
        {
          params: { ids: [id] },
          paramsSerializer: params => require('qs').stringify(params, { arrayFormat: 'repeat' }),
        },
      )
      return res.items.length ? res.items[0] : {}
    },
    async loadPerson() {
      const { person_code: personCode } = this.$route.params
      return await this.$axios.$get(`/person/${personCode}`)
    },
    onSearch(term) {
      this.$router.push(
        { path: '/', query: { s: term } },
      )
    },
    getMetaDescription() {
      const description = []
      const {
        first_name: firstName,
        middle_name: middleName,
        last_name: lastName,
        birthday,
        military,
      } = this.person
      description.push([lastName, firstName, middleName].filter(v => !!v).join(' '))
      if (birthday) {
        description.push(formatDateTime(birthday, { year: 'numeric', month: 'long', day: 'numeric' }) + 'р.')
      }
      description.push('')
      if (military) {
        description.push([RANKS[military.rank], military.post].filter(v => !!v).join(', '))
      }

      if (this.unit) {
        description.push(
          [this.unit.number ? 'в/ч ' + this.unit.number : null, this.unit.name].filter(v => !!v).join(', '),
        )
      }

      return description.join('\\n')
    },
  },
}
</script>
