<template>
  <v-form ref="formStepCrypto" v-model="valid">
    <v-container>
      <v-row class="mb-6">
        <span class="subtitle-1">
          Erstelle hier deinen persönlichen
          <span class="red--text">Gehmeim Schlüssel</span>
          damit nur der Besitzer dieses Schlüssels die persönlichen Daten
          deiner Teilnehmer sehen kann. <br />
          Dieser Schlüssel ist <span class="red--text">zwingend</span>
          erforderlich um die persönlichen
          Daten deiner Teilnehmer sehen zu können.<br /> <br>
          <span class="red--text">ACHTUNG:</span> <br> Wenn du diesen
          verlierst können die Daten deiner Teilnehmer <br>
          <span class="red--text">nie wieder </span>  lesbar gemacht werden. <br> <br>
          Bitte versende den Schlüssel <span class="red--text"> niemals per
          E-Mail </span> und sorge dafür dass er nicht verloren geht.
        </span>
      </v-row>
      <v-btn
        @click="onCreateKeysClick"
      >
      <v-icon left>
        mdi-key
      </v-icon>
        Erstelle Schlüssel
      </v-btn>
      <v-row>
        <v-textarea
          auto-grow
          readonly
          background-color="red lighten-3"
          v-model="data.privateKey"
          prepend-icon="mdi-shield-lock"
          label="Gemeiner Schlüssel"
          required />
      </v-row>

      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep()"
        @submitStep="submitStep()"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

const keypair = require('keypair');

export default {
  name: 'StepCrypto',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    data: {
      publicKey: null,
      privateKey: null,
    },
  }),
  validations: {
    data: {
      privateKey: {
        required,
      },
    },
  },
  computed: {
    buttonDisbabled() {
      return this.data.privateKey === null;
    },
  },
  methods: {
    onCreateKeysClick() {
      this.data.privateKey = null;
      const pair = keypair();
      this.data.privateKey = pair.private;
      this.data.publicKey = pair.public;
      this.isLoading = false;
      // const byteString = publicKey.encrypt('123');
      // console.log(ciphertext);

      // const base64String = forge.util.encode64(byteString);
      // console.log(base64String);
      // const byteString2 = forge.util.decode64(base64String);

      // const plaintext = privateKey.decrypt(byteString2);
      // console.log(plaintext);
    },
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$error;
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('nextStep');
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    getData() {
      return {
        publicKey: this.data.publicKey,
      };
    },
  },
};
</script>
