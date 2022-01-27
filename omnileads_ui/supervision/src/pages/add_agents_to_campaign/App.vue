<template>
  <div id="app">
    <router-view />
  </div>
</template>

   
<script>
import Cookies from "universal-cookie";
const cookies = new Cookies();

export default {
  name: "app",
  methods: {
    listenCookieChange(callback, interval = 1000) {
      let lastCookie = cookies.get("django_language");
      setInterval(() => {
        let cookie = cookies.get("django_language");
        if (cookie !== lastCookie) {
          try {
            callback({ oldValue: lastCookie, newValue: cookie });
          } finally {
            lastCookie = cookie;
          }
        }
      }, interval);
    },
  },
  mounted() {
    this.listenCookieChange(({ oldValue, newValue }) => {
      console.log(`---> Cambiar lenguaje de "${oldValue}" a "${newValue}"`);
      this.$i18n.locale = newValue;
    }, 1000);
  },
};
</script>