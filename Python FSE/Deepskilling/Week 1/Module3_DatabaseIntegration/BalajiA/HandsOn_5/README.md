# HANDS-ON 5: MongoDB — Document Modelling, CRUD & Aggregation

**Author:** Balaji A

## Topic

MongoDB Document Modelling, CRUD Operations, Aggregation Pipeline, Indexing, and Embedding vs Referencing.

## Output

> **Screenshots of the following are attached below:**
>
> <img width="1798" height="1020" alt="Screenshot 2026-07-02 105549" src="https://github.com/user-attachments/assets/b6d49899-bae2-4186-b75a-a2aade92eed7" />
<img width="1719" height="1023" alt="Screenshot 2026-07-02 105509" src="https://github.com/user-attachments/assets/1b8eed4d-4a47-43f4-ae55-55f87c45984e" />
<img width="1741" height="1020" alt="Screenshot 2026-07-02 105427" src="https://github.com/user-attachments/assets/fe45eed9-80f4-468b-b23a-fe884b6b9e85" />
<img width="1691" height="921" alt="Screenshot 2026-07-02 105010" src="https://github.com/user-attachments/assets/b249dc22-7eee-40d0-9c0d-bb66b8f54d55" />


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
