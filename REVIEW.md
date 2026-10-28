# REVIEW.md

## Out of scope

Do not review generated code blocks inside `**/ocp_resources/**` that fall
between:

- Start marker: `# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md`
- End marker: `# End of generated code`

This is auto-generated code from the class-generator tool. Only review code
outside these markers.

## Repository-specific rules

If someone modifies generated code directly (between the markers above),
flag it as a violation — changes should be made to the class-generator tool
instead, not the generated output.
