#!/usr/bin/python

import logging


def filter_variants_somatic(config_parameters, number_after_amplicons_all, new_variant_info_field, variant,
                            nr_amplicons_design, reads_all, pass_var_position_read_list):

    try:
        total_count_ratio = (100 * reads_all['total_read_var']['bam_normal'] / float(reads_all['total_quality_reads']['bam_normal']))
    except ZeroDivisionError:
        total_count_ratio = 0
    try:
        total_read_pos_ratio = (100 * (pass_var_position_read_list['passed']['bam_tumor']) / float(reads_all['total']['bam_tumor']))
    except ZeroDivisionError:
        total_read_pos_ratio = 100

    if variant.INFO['SS'] == '2' and total_count_ratio >= 10 and variant.samples[0]['DP'] >= 100:
        variant.add_filter('NormalFail')

    elif variant.INFO['SS'] == '2' and total_read_pos_ratio <= 10:
        variant.add_filter('PositionFail')

    elif variant.INFO['SS'] == '3' and total_read_pos_ratio <= 10:
        variant.add_filter('PositionFail')

    elif nr_amplicons_design < 2:
        variant.add_filter('OneAmpPass')

    else:
        if number_after_amplicons_all['total_amps']['bam_tumor'] <= 2:
            if number_after_amplicons_all['ref_amps']['bam_tumor'] == 2 and number_after_amplicons_all['alt_amps']['bam_tumor'] == 1 and number_after_amplicons_all['total_amps']['bam_tumor'] >= 1:
                variant.add_filter('MatchAmpPass')

            elif number_after_amplicons_all['ref_amps']['bam_tumor'] == 1 and number_after_amplicons_all['alt_amps']['bam_tumor'] == 2 and number_after_amplicons_all['total_amps']['bam_tumor'] >= 1:
                variant.add_filter('MatchAmpPass')

            elif number_after_amplicons_all['ref_amps']['bam_tumor'] == 1 and number_after_amplicons_all['alt_amps']['bam_tumor'] == 1 and number_after_amplicons_all['total_amps']['bam_tumor'] == 1:
                variant.add_filter('MatchAmpPass')

            elif number_after_amplicons_all['ref_amps']['bam_tumor'] == 2 and number_after_amplicons_all['alt_amps']['bam_tumor'] == 2 and number_after_amplicons_all['total_amps']['bam_tumor'] == 2:
                variant.add_filter('MatchAmpPass')

            else:
                variant.add_filter('LowAmpFail')

        elif variant.INFO['SS'] == '3' or variant.INFO['SS'] == '1' and number_after_amplicons_all['total_amps']['bam_tumor'] > 2:
            variant.add_filter('AmpPass')

        elif variant.INFO['SS'] == '2' or variant.INFO['SS'] == '5' and number_after_amplicons_all['alt_amps']['bam_tumor'] > 2:
            variant.add_filter('AmpPass')

        else:
            variant.add_filter('LowAmpFail')

    return variant


def add_variant_info_fields(number_after_amplicons_all, new_variant_info_field, variant):
    variant.add_info('AmpFA_n', new_variant_info_field['ampF_A']['bam_normal'])
    variant.add_info('AmpFR_n', new_variant_info_field['ampF_R']['bam_normal'])
    variant.add_info('AmpCA_n', number_after_amplicons_all['alt_amps']['bam_normal'])
    variant.add_info('AmpCR_n', number_after_amplicons_all['ref_amps']['bam_normal'])
    variant.add_info('AmpC_n', number_after_amplicons_all['total_amps']['bam_normal'])
    variant.add_info('AmpFA_t', new_variant_info_field['ampF_A']['bam_tumor'])
    variant.add_info('AmpFR_t', new_variant_info_field['ampF_A']['bam_tumor'])
    variant.add_info('AmpCA_t', number_after_amplicons_all['alt_amps']['bam_tumor'])
    variant.add_info('AmpCR_t', number_after_amplicons_all['ref_amps']['bam_tumor'])
    variant.add_info('AmpC_t', number_after_amplicons_all['total_amps']['bam_tumor'])

    return variant





    #if 'AD' in variant.FORMAT and len(variant.alleles) == 2:
     #   offset[var_type]['ref'].append(abs(refs - variant.samples[1]['RD']))
      #  dp[var_type]['ref'].append(variant.samples[1]['RD'])
       # offset[var_type]['alt'].append(abs(variant.samples[1]['AD']))
        #dp[var_type]['alt'].append(variant.samples[1]['AD'])
        # add to variant record.
  #      AmpF_O_R = refs - variant.samples[1]['RD']
   #     AmpF_O_A = alts - variant.samples[1]['AD']
    #    variant.add_info('AmpF_OR', AmpF_O_R)
     #   variant.add_info('AmpF_OA', AmpF_O_A)

#        if variant.INFO['AmpF_OA'] < -5:
 #           nr_offset += 1
  #          if 'STR' in variant.INFO:
   #             nr_str_offset += 1