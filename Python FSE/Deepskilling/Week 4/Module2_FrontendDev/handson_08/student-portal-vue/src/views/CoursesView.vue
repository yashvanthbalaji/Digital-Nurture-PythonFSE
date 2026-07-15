<template>
  <div class="page">
    <h1>Enrolled Courses</h1>

    <input
      type="text"
      placeholder="Search courses..."
      v-model="searchTerm"
    >

    <div class="course-grid">
      <div v-for="course in filteredCourses" :key="course.id" class="course-card-wrapper">
        <RouterLink :to="`/courses/${course.id}`">
          <CourseCard
            :name="course.name"
            :code="course.code"
            :credits="course.credits"
            :grade="course.grade"
          />
        </RouterLink>
        <button @click="handleEnroll(course)">Enroll</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import CourseCard from '../components/CourseCard.vue';
import { courses as courseData } from '../data';
import { useEnrollmentStore } from '../stores/enrollment';

const courses = ref([]);
const searchTerm = ref('');
const store = useEnrollmentStore();

onMounted(() => {
  courses.value = courseData;
});

// computed only re-runs when courses or searchTerm actually change
const filteredCourses = computed(() =>
  courses.value.filter(course =>
    course.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
);

function handleEnroll(course) {
  store.enroll(course);
}
</script>

<style scoped>
.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-top: 16px;
}
.course-card-wrapper a { text-decoration: none; color: inherit; display: block; }
</style>