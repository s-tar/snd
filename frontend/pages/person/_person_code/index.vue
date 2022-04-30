<script>
import Listing from '~/components/Listing'
import PersonCard from '~/components/Listing/ListItems/PersonCard'
import { RESPONSE_STATUS } from '~/utils/response_status'

export default {
  extends: Listing,
  auth: false,
  data() {
    return {
      person: {},
      unit: {},
    }
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
        this.unit = await this.loadMilitaryUnit(this.person.military.unit)
      }

      if (this.unit) {
        this.person.military.unitData = this.unit
      }

      this.person.showFullInfo = true
      this.loading = false
    },
    async loadMilitaryUnit(id) {
      const res = await this.$axios.$get(
        '/unit/get',
        {
          params: { id },
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
  },
}
</script>
