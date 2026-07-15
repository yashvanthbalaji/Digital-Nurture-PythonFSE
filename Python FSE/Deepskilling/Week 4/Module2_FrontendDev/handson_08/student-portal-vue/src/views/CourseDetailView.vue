<template>
  <div class="page">
    <div v-if="course">
      <h1>{{ course.name }}</h1>
      <p>Course code: {{ course.code }}</p>
      <p>Credits: {{ course.credits }}</p>
      <p>Grade: {{ course.grade }}</p>
      <button @click="handleEnroll">Enroll</button>
    </div>
    <p v-else>Course not found.</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { courses } from '../data';
import { useEnrollmentStore } from '../stores/enrollment';

const route = useRoute();
const router = useRouter();
const store = useEnrollmentStore();

// route.params.id always comes back as a string, so convert it to compare
const course = computed(() =>
  courses.find(c => c.id === Number(route.params.id))
);

function handleEnroll() {
  store.enroll(course.value);
  router.push('/profile');
}
</script>