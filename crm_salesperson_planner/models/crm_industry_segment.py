# Copyright 2021 Sygel - Valentin Vinagre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class CrmIndustrySegment(models.Model):
    _name = "crm.industry.segment"
    _description = "Customer Industry Segment"

    name = fields.Char(string="Description", required=True)
    code = fields.Char(string="Code", required=True)
    job_nature_ids = fields.One2many(
        'crm.job.nature', 'industry_segment_id', string='Nature of Job')


class CrmJobNature(models.Model):
    _name = 'crm.job.nature'

    name = fields.Char(string='Description')
    industry_segment_id = fields.Many2one(
        'crm.industry.segment', string='Industry Segment', required=True)
    occupation_ids = fields.One2many(
        'crm.occupation', 'job_nature_id', string='Occupation')


class CrmOccupation(models.Model):
    _name = 'crm.occupation'

    name = fields.Char(string='Description')
    job_nature_id = fields.Many2one(
        'crm.job.nature', string='Nature of Job', required=True)
