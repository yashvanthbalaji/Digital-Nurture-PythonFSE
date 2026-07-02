// Digital Nurture 5.0 | Module 3: Database Integration
// Hands-On 5: MongoDB - Document Modelling, CRUD & Aggregation
// Name   : BALAJI A

// TASK 1: Create Collection and Insert Documents

// Step 60: Create database
use('college_nosql');

// Step 61 & 62: Create feedback collection and insert 10 documents

db.feedback.insertMany([
    {
        student_id   : 1,
        course_code  : 'CS101',
        semester     : '2022-ODD',
        rating       : 4,
        comments     : 'Excellent teaching. Would recommend.',
        tags         : ['challenging', 'well-structured', 'good-examples'],
        submitted_at : new Date('2022-11-30T10:15:00Z'),
        attachments  : [{ filename: 'notes.pdf', size_kb: 240 }]
    },
    {
        student_id   : 2,
        course_code  : 'CS101',
        semester     : '2022-ODD',
        rating       : 5,
        comments     : 'Very well explained. Best course so far.',
        tags         : ['challenging', 'interesting', 'good-examples'],
        submitted_at : new Date('2022-11-28T09:00:00Z'),
        attachments  : [{ filename: 'assignment1.pdf', size_kb: 180 }]
    },
    {
        student_id   : 3,
        course_code  : 'CS101',
        semester     : '2022-ODD',
        rating       : 2,
        comments     : 'Concepts were hard to follow. Needs improvement.',
        tags         : ['difficult', 'needs-improvement'],
        submitted_at : new Date('2022-11-29T14:30:00Z'),
        attachments  : [{ filename: 'feedback.pdf', size_kb: 90 }]
    },
    {
        student_id   : 1,
        course_code  : 'CS102',
        semester     : '2022-ODD',
        rating       : 3,
        comments     : 'Average course. Could be more practical.',
        tags         : ['average', 'well-structured'],
        submitted_at : new Date('2022-12-01T11:00:00Z'),
        attachments  : [{ filename: 'notes2.pdf', size_kb: 150 }]
    },
    {
        // Step 63: Intentionally omitting attachments field
        student_id   : 2,
        course_code  : 'CS102',
        semester     : '2022-ODD',
        rating       : 5,
        comments     : 'Loved it! Great professor.',
        tags         : ['interesting', 'good-examples'],
        submitted_at : new Date('2022-12-02T08:45:00Z')
    },
    {
        student_id   : 4,
        course_code  : 'CS103',
        semester     : '2021-EVEN',
        rating       : 1,
        comments     : 'Very difficult to understand. Not helpful.',
        tags         : ['difficult', 'needs-improvement'],
        submitted_at : new Date('2021-05-10T10:00:00Z'),
        attachments  : [{ filename: 'oop_notes.pdf', size_kb: 200 }]
    },
    {
        student_id   : 3,
        course_code  : 'EC101',
        semester     : '2022-ODD',
        rating       : 4,
        comments     : 'Good content. Practical sessions were helpful.',
        tags         : ['interesting', 'well-structured'],
        submitted_at : new Date('2022-11-25T13:00:00Z'),
        attachments  : [{ filename: 'circuit_notes.pdf', size_kb: 310 }]
    },
    {
        student_id   : 5,
        course_code  : 'ME101',
        semester     : '2021-EVEN',
        rating       : 2,
        comments     : 'Needs more lab sessions.',
        tags         : ['average', 'needs-improvement'],
        submitted_at : new Date('2021-05-15T15:30:00Z'),
        attachments  : [{ filename: 'thermo_notes.pdf', size_kb: 120 }]
    },
    {
        student_id   : 5,
        course_code  : 'CS101',
        semester     : '2022-EVEN',
        rating       : 5,
        comments     : 'Wonderful experience. Highly recommended!',
        tags         : ['challenging', 'interesting', 'good-examples'],
        submitted_at : new Date('2022-05-20T09:30:00Z'),
        attachments  : [{ filename: 'dsa_notes.pdf', size_kb: 400 }]
    },
    {
        student_id   : 6,
        course_code  : 'CS102',
        semester     : '2022-ODD',
        rating       : 3,
        comments     : 'Good but needs more assignments.',
        tags         : ['average', 'well-structured'],
        submitted_at : new Date('2022-12-05T10:00:00Z'),
        attachments  : [{ filename: 'dbms_notes.pdf', size_kb: 260 }]
    }
]);

// Step 64: Verify total document count
db.feedback.countDocuments();


// TASK 2: CRUD Operations

// Step 65: READ - Find all documents where rating is 5
db.feedback.find({ rating: 5 });

// Step 66: READ - CS101 feedback where tags contains 'challenging'
db.feedback.find({ course_code: 'CS101', tags: 'challenging' });

// Step 67: READ - Projection: only student_id, course_code, rating (no _id)
db.feedback.find({}, { student_id: 1, course_code: 1, rating: 1, _id: 0 });

// Step 68: UPDATE - Add needs_review: true for all documents with rating < 3
db.feedback.updateMany(
    { rating: { $lt: 3 } },
    { $set: { needs_review: true } }
);

// Step 69: UPDATE - Push 'reviewed' tag into tags array where needs_review is true
db.feedback.updateMany(
    { needs_review: true },
    { $push: { tags: 'reviewed' } }
);

// Step 70: DELETE - Remove all documents where semester is '2021-EVEN'
db.feedback.deleteMany({ semester: '2021-EVEN' });


// TASK 3: Aggregation Pipeline

// Step 71: Pipeline - filter 2022-ODD, group by course_code, sort by avg rating
db.feedback.aggregate([
    { $match: { semester: '2022-ODD' } },
    {
        $group: {
            _id          : '$course_code',
            avg_rating   : { $avg: '$rating' },
            feedback_count: { $sum: 1 }
        }
    },
    { $sort: { avg_rating: -1 } }
]);

// Step 72: Extended pipeline with $project to rename and round avg_rating
db.feedback.aggregate([
    { $match: { semester: '2022-ODD' } },
    {
        $group: {
            _id           : '$course_code',
            avg_rating    : { $avg: '$rating' },
            feedback_count: { $sum: 1 }
        }
    },
    { $sort: { avg_rating: -1 } },
    {
        $project: {
            _id            : 1,
            feedback_count : 1,
            average_rating : { $round: ['$avg_rating', 1] }
        }
    }
]);

// Step 73: Tag frequency leaderboard using $unwind and $group
db.feedback.aggregate([
    { $unwind: '$tags' },
    {
        $group: {
            _id  : '$tags',
            count: { $sum: 1 }
        }
    },
    { $sort: { count: -1 } }
]);

// Step 74: Create index on course_code
db.feedback.createIndex({ course_code: 1 });

// Verify index usage - confirm IXSCAN not COLLSCAN
db.feedback.find({ course_code: 'CS101' }).explain('executionStats');



// END OF HANDS-ON 5
