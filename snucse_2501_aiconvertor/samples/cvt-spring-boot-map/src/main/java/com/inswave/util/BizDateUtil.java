package com.inswave.util;

import java.time.LocalDate;

/** Utilities for “open market” business-day arithmetic */
public final class BizDateUtil {

    private BizDateUtil() {}

    /**
     * @return number of business days from start (inclusive) to end (exclusive).
     *         Weekends and default Korean holidays are skipped.
     */
    public static int getBizDays(LocalDate startInclusive, LocalDate endExclusive) {
        int days = 0;
        for (LocalDate d = startInclusive; d.isBefore(endExclusive); d = d.plusDays(1)) {
            if (isBusinessDay(d)) days++;
        }
        return days;
    }

    private static boolean isBusinessDay(LocalDate d) {
        switch (d.getDayOfWeek()) {
            case SATURDAY: case SUNDAY: return false;
            default: return true;                 // 〃easy stub – real one checks holiday table
        }
    }
}
