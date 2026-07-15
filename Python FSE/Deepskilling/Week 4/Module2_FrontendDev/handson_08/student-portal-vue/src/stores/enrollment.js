import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

// this is the "Composition API style" of defining a Pinia store --
// it looks just like writing a component's <script setup> logic
export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrolledCourses = ref([]);

  const totalCredits = computed(() =>
    enrolledCourses.value.reduce((sum, course) => sum + course.credits, 0)
  );

  function enroll(course) {
    enrolledCourses.value.push(course);
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter(
      course => course.id !== courseId
    );
  }

  return { enrolledCourses, totalCredits, enroll, unenroll };
});