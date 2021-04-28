<template>
  <div>
    <h5>
      Generiere hier verschiedene PDFs. Es dauert etwas, bis es fertig geladen ist.
      Nach dem Klick auf den Button, beginnt der Download. Die Daten werden auf PDFs mit
      jeweils maximal 100 Einträgen und 10 Seiten aufgeteilt.
    </h5>
    <v-container>
      <v-btn :disabled="!pdfContentIsReady" @click="generatePdf()"> generiere pdf</v-btn>
      <v-progress-circular
        v-if="pdfIsGenerating"
        class="ml-3"
        color="primary"
        indeterminate
      />
      <v-progress-linear v-if="!pdfContentIsReady" class="mt-3" indeterminate />
      <pdf-content-page
        ref="pdfContentPage"
        @loadingDone="updatePage()"
      />
    </v-container>
  </div>
</template>

<script>
import pdfContentPage from '@/views/statistic/downlaods/tabs/pdf/ContentPage.vue';
import html2pdf from 'html2pdf.js';

export default {
  name: 'pdfGeneration',
  components: { pdfContentPage },
  data: () => ({
    pdfContentIsReady: false,
    pdfIsGenerating: false,
    documentCounter: 0,
  }),
  computed: {
    htmlToPdfOptions() {
      const { groupsPerDocument } = this.$refs.pdfContentPage.$data;
      const maxLength = this.$refs.pdfContentPage.$data.allGroups.length;
      const min = this.documentCounter * groupsPerDocument + 1;
      const max = (min + groupsPerDocument > maxLength) ? maxLength : min + groupsPerDocument - 1;

      const filename = `stämme${min}_${max}.pdf`;
      return {
        filename,
        enableLinks: true,
        html2canvas: {
          useCORS: true,
        },
      };
    },
  },
  methods: {
    updatePage() {
      this.pdfContentIsReady = true;
      this.$forceUpdate();
    },
    async generatePdf() {
      this.pdfIsGenerating = true;
      await this.$refs.pdfContentPage.setCurrent(this.documentCounter);
      await html2pdf().from(this.$refs.pdfContentPage.$el).set(this.htmlToPdfOptions).save();
      await this.afterDownload();
      this.pdfIsGenerating = false;
    },
    async afterDownload() {
      const { groupsPerDocument, allGroups } = this.$refs.pdfContentPage.$data;
      this.documentCounter += 1;
      if (allGroups.length / groupsPerDocument > this.documentCounter) {
        await this.generatePdf(); // generates next pdf document (e.g. recursion)
      } else {
        // resets DOM
        this.documentCounter = 0;
        this.pdfContentIsReady = false;
        await this.$refs.pdfContentPage.setCurrent(this.documentCounter);
      }
    },
  },
};
</script>
