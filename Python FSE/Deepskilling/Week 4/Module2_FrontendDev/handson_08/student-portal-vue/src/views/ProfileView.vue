<template>
  <div class="page">
    <h1>My Profile</h1>

    <h2>Enrolled Courses</h2>
    <p v-if="store.enrolledCourses.length === 0">
      You haven't enrolled in any courses yet.
    </p>
    <ul>
      <li v-for="course in store.enrolledCourses" :key="course.id">
        {{ course.name }} ({{ course.code }})
        <button @click="store.unenroll(course.id)">Remove</button>
      </li>
    </ul>

    <p>Total credits: {{ store.totalCredits }}</p>
  </div>
</template>

<script setup>
import { useEnrollmentStore } from '../stores/enrollment';

const store = useEnrollmentStore();
</script>