import json

from datetime import datetime

from .exceptions import ValidationError


class AutomationSchemaValidation:
    def __init__(self, schema_path):
        self.schema_path = schema_path

    def read_schema(self):
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValidationError(
                'Schema file not found', self.schema_path)
        except json.JSONDecodeError:
            raise ValidationError(
                'Invalid JSON in schema file', self.schema_path)
        except Exception as e:
            raise ValidationError(
                'An error occurred while reading schema file', e)

    def validate(self):
        schema = self.read_schema()
        self.validate_schema(schema)

    def validate_schema(self, rules: list) -> list:
        for rule in rules:
            self.validate_rule(rule)
        return rules

    def _validate_rule(self, rule: dict) -> dict:
        name = rule.get('name', '')
        if not name:
            raise ValidationError(
                'Rule name is required in rule', rule)

        description = rule.get('description', '')
        if not description:
            raise ValidationError(
                'Rule description is required in rule', rule)

        conditions = rule.get('conditions', [])
        if not conditions:
            raise ValidationError(
                'Rule conditions are required in rule', rule)

        actions = rule.get('actions', [])
        if not actions:
            raise ValidationError(
                'Rule actions are required in rule', rule)

        return {
            "name": name,
            "description": description,
            "conditions": conditions,
            "actions": actions
        }

    def validate_rule(self, rule):
        validated_rule = self._validate_rule(rule)
        self.validate_conditions(validated_rule['conditions'])
        self.validate_actions(validated_rule['actions'])

    def validate_conditions(self, conditions: list):
        for condition in conditions:
            self.validate_condition(condition)

    def _validate_condition(self, condition: dict) -> dict:
        condition_type = condition.get('type', '')
        if not condition_type:
            raise ValidationError(
                'Condition type is required', condition)

        field = condition.get('field', '')
        if not field:
            raise ValidationError(
                'Field is required in condition', condition)

        if field not in ['from', 'to', 'subject', 'date_received']:
            raise ValidationError(
                f'Invalid field: {field}', condition)

        operator = condition.get('operator', '')
        if not operator:
            raise ValidationError(
                'Operator is required in condition', condition)

        value = condition.get('value', '')
        if not value:
            raise ValidationError(
                'Value is required in condition', condition)

        return {
            "type": condition_type,
            "field": field,
            "operator": operator,
            "value": value
        }

    def validate_condition(self, condition: dict):
        validated_condition = self._validate_condition(condition)
        field = validated_condition['field']

        if field in ['from', 'to', 'subject']:
            self._validate_string_condition(validated_condition)
        elif field == 'date_received':
            self._validate_datetime_condition(validated_condition)
        else:
            raise ValidationError(
                f'Invalid field type: {field}', condition)

        return validated_condition

    def _validate_string_condition(self, condition: dict):
        operator = condition['operator']
        if operator not in ['eq', 'neq', 'contains', 'ncontains']:
            raise ValidationError(
                f'Invalid operator: {operator}', condition)

        value = condition['value']
        if not isinstance(value, str):
            raise ValidationError(
                'Value must be a string', condition)

    def _validate_datetime_condition(self, condition: dict):
        operator = condition['operator']
        if operator not in ['lt', 'gt', 'eq', 'neq']:
            raise ValidationError(
                f'Invalid operator: {operator}', condition)

        value = condition['value']
        if operator in ['lt', 'gt']:
            if not isinstance(value, int):  # Days
                raise ValidationError(
                    'Value must be a int as days', condition)

        if operator in ['eq', 'neq']:
            if not isinstance(value, str):
                raise ValidationError(
                    'Value must be a string', condition)

            allowed_formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S']
            for format in allowed_formats:
                try:
                    datetime.strptime(value, format)
                    break
                except ValueError:
                    pass
            else:
                raise ValidationError(
                    'Invalid datetime format', condition)

    def validate_actions(self, actions: list):
        for action in actions:
            self.validate_action(action)

    def _validate_action(self, action: dict):
        action_type = action.get('type', '')
        if not action_type:
            raise ValidationError(
                'Action type is required', action)

        if action_type not in ['forward', 'archive', 'trash']:
            raise ValidationError(
                f'Invalid action type: {action_type}', action)

        return action

    def validate_action(self, action: dict):
        validated_action = self._validate_action(action)
        action = validated_action['action']

        if action == 'mark_as_read':
            self._validate_mark_as_read(validated_action)
        elif action == 'mark_as_unread':
            self._validate_mark_as_unread(validated_action)
        elif action == 'move_to':
            self._validate_move_to(validated_action)
        else:
            raise ValidationError(
                f'Invalid action: {action}', action)

        return action

    def _validate_mark_as_read(self, action: dict):
        pass  # No validation required

    def _validate_mark_as_unread(self, action: dict):
        pass  # No validation required

    def _validate_move_to(self, action: dict):
        mailbox = action.get('mailbox', '')
        if not mailbox:
            raise ValidationError(
                'Mailbox is required in move_to action', action)
