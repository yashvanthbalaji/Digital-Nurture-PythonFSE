# HANDS-ON 5: MongoDB — Document Modelling, CRUD & Aggregation

**Author:** Balaji A

## Topic

MongoDB Document Modelling, CRUD Operations, Aggregation Pipeline, Indexing, and Embedding vs Referencing.

## Output

> **Screenshots of the following are attached below:**

* MongoDB database (`college_nosql`) and `feedback` collection creation
* Insertion of feedback documents
* Verification using `countDocuments()`
* CRUD operation outputs (Find, Update, Delete)
* Aggregation Pipeline results
* Tag frequency leaderboard
* Index creation on `course_code`
* `explain('executionStats')` output showing `IXSCAN`

## Result

* Successfully created the MongoDB database and feedback collection.
* Inserted multiple feedback documents with varying ratings, semesters, and tags.
* Demonstrated MongoDB's schema flexibility by inserting a document without the `attachments` field.
* Performed all CRUD operations successfully.
* Built aggregation pipelines to generate course-wise rating reports and tag frequency analysis.
* Created an index on `course_code` and verified improved query performance using `IXSCAN`.
* Gained practical experience with MongoDB document modelling, aggregation, and indexing.
