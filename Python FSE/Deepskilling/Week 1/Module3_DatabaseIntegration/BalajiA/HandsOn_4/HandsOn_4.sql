-- Digital Nurture 5.0 | Module 3: Database Integration
-- Hands-On 4: Query Optimisation - Indexes, EXPLAIN & N+1
-- Name   : BALAJI A
-- ============================================================

USE college_db;

-- TASK 1: Baseline Performance — No Indexes

-- Step 48
EXPLAIN FORMAT=JSON
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses  c ON c.course_id  = e.course_id
WHERE s.enrollment_year = 2022;

-- Paste your EXPLAIN FORMAT=JSON output here:
/* {
    "query_block": {
        "select_id": 1,
        "cost_info": {
            "query_cost": "2.12"
        },
        "nested_loop": [
            {
                "table": {
                    "table_name": "s",
                    "access_type": "ALL",
                    "possible_keys": [
                        "PRIMARY"
                    ],
                    "rows_examined_per_scan": 10,
                    "rows_produced_per_join": 1,
                    "filtered": "10.00",
                    "cost_info": {
                        "read_cost": "1.15",
                        "eval_cost": "0.10",
                        "prefix_cost": "1.25",
                        "data_read_per_join": "824"
                    },
                    "used_columns": [
                        "student_id",
                        "first_name",
                        "last_name",
                        "enrollment_year"
                    ],
                    "attached_condition": "(`college_db`.`s`.`enrollment_year` = 2022)"
                }
            },
            {
                "table": {
                    "table_name": "e",
                    "access_type": "ref",
                    "possible_keys": [
                        "student_id",
                        "course_id"
                    ],
                    "key": "student_id",
                    "used_key_parts": [
                        "student_id"
                    ],
                    "key_length": "5",
                    "ref": [
                        "college_db.s.student_id"
                    ],
                    "rows_examined_per_scan": 1,
                    "rows_produced_per_join": 1,
                    "filtered": "100.00",
                    "cost_info": {
                        "read_cost": "0.31",
                        "eval_cost": "0.13",
                        "prefix_cost": "1.69",
                        "data_read_per_join": "40"
                    },
                    "used_columns": [
                        "student_id",
                        "course_id"
                    ],
                    "attached_condition": "(`college_db`.`e`.`course_id` is not null)"
                }
            },
            {
                "table": {
                    "table_name": "c",
                    "access_type": "eq_ref",
                    "possible_keys": [
                        "PRIMARY"
                    ],
                    "key": "PRIMARY",
                    "used_key_parts": [
                        "course_id"
                    ],
                    "key_length": "4",
                    "ref": [
                        "college_db.e.course_id"
                    ],
                    "rows_examined_per_scan": 1,
                    "rows_produced_per_join": 1,
                    "filtered": "100.00",
                    "cost_info": {
                        "read_cost": "0.31",
                        "eval_cost": "0.13",
                        "prefix_cost": "2.13",
                        "data_read_per_join": "880"
                    },
                    "used_columns": [
                        "course_id",
                        "course_name"
                    ]
                }
            }
        ]
    }
}

*/

-- Step 49
-- Full Table Scan observed on: students (table alias: s)
-- access_type: "ALL" confirms Full Table Scan (no index used)

-- Step 50
-- Total query cost    : 2.12
-- Rows examined (s)   : 10  (full scan on students)
-- Rows examined (e)   : 1   (used index: student_id)
-- Rows examined (c)   : 1   (used PRIMARY key)


-- TASK 2: Add Indexes and Compare Plans

-- Step 51: B-Tree index on students.enrollment_year
CREATE INDEX idx_enrollment_year ON students(enrollment_year);

-- Step 52: Composite UNIQUE index on enrollments(student_id, course_id)
CREATE UNIQUE INDEX idx_student_course ON enrollments(student_id, course_id);

-- Step 53: Index on courses.course_code
CREATE INDEX idx_course_code ON courses(course_code);

-- Step 54: Re-run same EXPLAIN and compare with baseline
EXPLAIN FORMAT=JSON
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses  c ON c.course_id  = e.course_id
WHERE s.enrollment_year = 2022;

-- Paste new EXPLAIN output here:
/*
{
  "query_block": {
    "select_id": 1,
    "cost_info": {
      "query_cost": "5.79"
    },
    "nested_loop": [
      {
        "table": {
          "table_name": "s",
          "access_type": "ref",
          "possible_keys": [
            "PRIMARY",
            "idx_enrollment_year"
          ],
          "key": "idx_enrollment_year",
          "used_key_parts": [
            "enrollment_year"
          ],
          "key_length": "5",
          "ref": [
            "const"
          ],
          "rows_examined_per_scan": 5,
          "rows_produced_per_join": 5,
          "filtered": "100.00",
          "cost_info": {
            "read_cost": "0.50",
            "eval_cost": "0.50",
            "prefix_cost": "1.00",
            "data_read_per_join": "4K"
          },
          "used_columns": [
            "student_id",
            "first_name",
            "last_name",
            "enrollment_year"
          ]
        }
      },
      {
        "table": {
          "table_name": "e",
          "access_type": "ref",
          "possible_keys": [
            "idx_student_course",
            "course_id"
          ],
          "key": "idx_student_course",
          "used_key_parts": [
            "student_id"
          ],
          "key_length": "5",
          "ref": [
            "college_db.s.student_id"
          ],
          "rows_examined_per_scan": 1,
          "rows_produced_per_join": 7,
          "filtered": "100.00",
          "using_index": true,
          "cost_info": {
            "read_cost": "1.25",
            "eval_cost": "0.79",
            "prefix_cost": "3.04",
            "data_read_per_join": "251"
          },
          "used_columns": [
            "student_id",
            "course_id"
          ],
          "attached_condition": "(`college_db`.`e`.`course_id` is not null)"
        }
      },
      {
        "table": {
          "table_name": "c",
          "access_type": "eq_ref",
          "possible_keys": [
            "PRIMARY"
          ],
          "key": "PRIMARY",
          "used_key_parts": [
            "course_id"
          ],
          "key_length": "4",
          "ref": [
            "college_db.e.course_id"
          ],
          "rows_examined_per_scan": 1,
          "rows_produced_per_join": 7,
          "filtered": "100.00",
          "cost_info": {
            "read_cost": "1.96",
            "eval_cost": "0.79",
            "prefix_cost": "5.79",
            "data_read_per_join": "5K"
          },
          "used_columns": [
            "course_id",
            "course_name"
          ]
        }
      }
    ]
  }
}
*/
 

-- Step 54: Re-run EXPLAIN after adding indexes

-- Comparison:
-- Before index: students → access_type: ALL (Full Table Scan) - rows_examined: 10 - query_cost: 2.12
-- After index:  students → access_type: ref (Index Scan: idx_enrollment_year) - rows_examined: 5 - query_cost: 5.79

-- Observation:
-- students table changed from ALL → ref (index is now being used)
-- enrollments table now uses idx_student_course instead of student_id index
-- Note: Total query cost increased (2.12 → 5.79) because table is small (10 rows only)
-- On large datasets, index scan will always be faster than full table scan

CREATE INDEX idx_enrollments_student_id ON enrollments(student_id);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- TASK 3: N+1 Problem — see n1_problem.py
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- END OF HANDS-ON 4
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━