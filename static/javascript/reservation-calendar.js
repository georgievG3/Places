document.addEventListener("DOMContentLoaded", function () {
    const calendarEl = document.getElementById("calendar");
    if (!calendarEl) return;

    const pageType = window.pageType || "listing";
    const checkInInput = document.getElementById("check-in") || document.querySelector('input[name="check_in"]');
    const checkOutInput = document.getElementById("check-out") || document.querySelector('input[name="check_out"]');
    const reserveBtn = document.getElementById("reserve-btn");

    const reservedRanges = window.reservedDates || [];
    let firstClickDate = null;

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    function isDateRangeAvailable(start, end) {
        return !reservedRanges.some((r) => !(end <= r.start || start >= r.end));
    }

    function highlightSelection(calendar, start, end) {
        const endDate = new Date(end);
        endDate.setDate(endDate.getDate() + 1);
        const calendarEndFormatted = endDate.toISOString().split("T")[0];

        calendar.getEvents().forEach((event) => {
            if (event.extendedProps && event.extendedProps.selected) {
                event.remove();
            }
        });

        calendar.addEvent({
            start: start,
            end: calendarEndFormatted,
            color: "green",
            display: "background",
            extendedProps: {
                selected: true,
            },
        });
    }

    window.calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        selectable: false,
        validRange: function() {
            if (pageType === "reservation") {
                const tomorrow = new Date(today);
                tomorrow.setDate(tomorrow.getDate() + 1);
                return { start: tomorrow };
            } else {
                return { start: today };
            }
        },
        events: reservedRanges.map((r) => ({
            start: r.start,
            end: r.end,
            color: "red",
            display: "background",
        })),
        dateClick: function (info) {
            const clickedDate = info.dateStr;
            const clicked = new Date(clickedDate);
            clicked.setHours(0, 0, 0, 0);

            if (!firstClickDate) {
                firstClickDate = clickedDate;
                checkInInput.value = clickedDate;
                checkOutInput.value = "";

                calendar.getEvents().forEach((event) => {
                    if (event.extendedProps && event.extendedProps.selected) {
                        event.remove();
                    }
                });

                calendar.addEvent({
                    start: clickedDate,
                    end: clickedDate,
                    color: "green",
                    display: "background",
                    extendedProps: {
                        selected: true,
                    },
                });

            } else {
                let start = firstClickDate;
                let end = clickedDate;
                if (start > end) [start, end] = [end, start];

                const startDate = new Date(start);
                const endDate = new Date(end);
                const diffDays = (endDate - startDate) / (1000 * 60 * 60 * 24);

                if (pageType === "reservation" && diffDays < 1) {
                    alert("Минималната резервация е 1 нощ.");
                    checkInInput.value = "";
                    checkOutInput.value = "";
                    firstClickDate = null;
                    return;
                }

                const endPlusOne = new Date(end);
                endPlusOne.setDate(endPlusOne.getDate() + 1);
                const endFormatted = endPlusOne.toISOString().split("T")[0];

                if (!isDateRangeAvailable(start, endFormatted)) {
                    alert("Избраният период съдържа заети дни.");
                    checkInInput.value = "";
                    checkOutInput.value = "";
                    firstClickDate = null;
                    return;
                }

                checkInInput.value = start;
                checkOutInput.value = end;

                highlightSelection(calendar, start, end);
                firstClickDate = null;
            }
        },
    });

    window.calendar.render();

    if (pageType === "listing" && reserveBtn) {
        reserveBtn.addEventListener("click", function (e) {
            e.preventDefault();
            const checkIn = checkInInput.value;
            const checkOut = checkOutInput.value;
            if (!checkIn || !checkOut) {
                alert("Моля, изберете валиден период.");
                return;
            }
            const baseUrl = reserveBtn.getAttribute("href");
            window.location.href = `${baseUrl}?check_in=${checkIn}&check_out=${checkOut}`;
        });
    }

    if (pageType === "reservation") {
        const prefillCheckIn = checkInInput?.value;
        const prefillCheckOut = checkOutInput?.value;
        if (prefillCheckIn && prefillCheckOut) {
            highlightSelection(calendar, prefillCheckIn, prefillCheckOut);
        }
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("filters-toggle-btn");
    const filtersModal = document.getElementById("filters-modal");
    const filtersContent = document.querySelector(".filters-content");

    if (!toggleBtn || !filtersModal || !filtersContent) return;

    toggleBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        filtersModal.classList.toggle("hidden");

        if (window.calendar && typeof window.calendar.updateSize === "function") {
            window.calendar.updateSize();
        }
    });

    filtersContent.addEventListener("click", function (e) {
        e.stopPropagation();
    });

    filtersModal.addEventListener("click", function () {
        filtersModal.classList.add("hidden");
    });
});
