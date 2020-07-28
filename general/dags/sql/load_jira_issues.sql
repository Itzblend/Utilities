INSERT INTO kafka_t.jira_issues_t (
    issue_id,
    issue_key,
    issue_type,
    parent_id,
    parent_key,
    project_id,
    project_key,
    project_type,
    summary,
    creator,
    reporter,
    created,
    updated,
    priority,
    status
)
SELECT
    (data ->> 'id')::INT AS issue_id,
    data ->> 'key' AS issue_key,
    data #>> '{{fields, issuetype, name}}' AS issue_type,
    (data #>> '{{fields, parent, id}}')::INT AS parent_id,
    data #>> '{{fields, parent, key}}' AS parent_key,
    (data #>> '{{fields, project, id}}')::INT AS project_id,
    data #>> '{{fields, project, key}}' AS project_key,
    data #>> '{{fields, project, projectTypeKey}}' AS project_type,
    data #>> '{{fields, summary}}' AS summary,
    data #>> '{{fields, creator, displayName}}' AS creator,
    data #>> '{{fields, reporter, displayName}}' AS reporter,
    (data #>> '{{fields, created}}')::TIMESTAMP AS created,
    (data #>> '{{fields, updated}}')::TIMESTAMP AS updated,
    data #>> '{{fields, priority, name}}' AS priority,
    data #>> '{{fields, status, name}}' AS status
FROM
    staging
ON CONFLICT DO NOTHING
