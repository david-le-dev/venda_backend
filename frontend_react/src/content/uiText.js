const shared = {
  en: {
    language: "Language",
    name: "Name",
    birthDate: "Birth date (Gregorian)",
    birthTime: "Birth time",
    birthPlace: "Birth place",
    gender: "Gender",
    question: "Question",
    faceUpload: "Upload face image",
    palmUpload: "Upload palm image",
    reportLanguage: "Report language",
    timeFocus: "Time focus",
    modeLabel: "Reading system ( choose 1)",
    nameHelp: "Required. Used to personalize the reading.",
    birthDateHelp: "Use your Gregorian birth date for consistency.",
    birthTimeHelp: "Optional. Pick hour, minute, and AM or PM. Use Unknown if you do not know it.",
    birthPlaceHelp: "City and country are enough for the demo.",
    genderHelp: "",
    questionHelp: "Open-ended prompts usually create stronger reflective output.",
    faceHelp: "Optional. Used for gentle symbolic presentation cues only.",
    palmHelp: "Optional. Used for symbolic palm-reading themes only.",
    timeFocusHelp: "Optional. Example: this year, next 6 months, 2026-2030.",
    analyze: "Analyze",
    analyzing: "The observatory is aligning the reading...",
    reset: "Reset",
    logsTitle: "Live Agent Logs",
    resultTitle: "Streaming Result",
    exportTitle: "Export",
    exportButton: "Export PDF",
    exportHint: "Downloads the current report from the backend export endpoint.",
    validationName: "A name is required.",
    validationDate: "Birth date is required.",
    validationPlace: "Birth place is required.",
    validationQuestion: "A question is required.",
    importantNote: "Important Note",
    errorPrefix: "Something went wrong",
    birthTimeLabels: {
      hour: "Hour",
      minute: "Minute",
      period: "AM/PM",
      unknown: "Unknown birth time",
    },
    genderOptions: {
      female: "Female",
      male: "Male",
      non_binary: "Non-binary",
      prefer_not_to_say: "Prefer not to say",
    },
    placeholders: {
      name: "Your name",
      birthPlace: "Vancouver, BC, Canada",
      question: "What should I focus on in love, work, and personal growth this year?",
      timeFocus: "This year or 2026-2030",
    },
  },
  vi: {
    language: "Ngôn ngữ",
    name: "Tên",
    birthDate: "Ngày sinh (dương lịch)",
    birthTime: "Giờ sinh",
    birthPlace: "Nơi sinh",
    gender: "Giới tính",
    question: "Câu hỏi",
    faceUpload: "Tải ảnh khuôn mặt",
    palmUpload: "Tải ảnh bàn tay",
    reportLanguage: "Ngôn ngữ báo cáo",
    timeFocus: "Mốc thời gian quan tâm",
    modeLabel: "Hệ đọc (chọn 1)",
    nameHelp: "Bắt buộc. Dùng để cá nhân hóa bản đọc.",
    birthDateHelp: "Vui lòng dùng ngày sinh dương lịch.",
    birthTimeHelp: "Không bắt buộc. Chọn giờ, phút, và AM hoặc PM. Nếu không nhớ thì chọn Chưa rõ.",
    birthPlaceHelp: "Thành phố và quốc gia.",
    genderHelp: "",
    questionHelp: "Câu hỏi mở thường cho ra kết quả tự nhiên hơn.",
    faceHelp: "Không bắt buộc. Chỉ dùng cho các dấu hiệu trình bày mang tính biểu tượng.",
    palmHelp: "Không bắt buộc. Chỉ dùng cho các chủ đề chỉ tay mang tính biểu tượng.",
    timeFocusHelp: "Không bắt buộc. Ví dụ: năm nay, 6 tháng tới, 2026-2030.",
    analyze: "Bắt Đầu",
    analyzing: "Hệ thống đang căn chỉnh bản đọc...",
    reset: "Nhập Lại",
    logsTitle: "Nhật Ký Agent",
    resultTitle: "Báo Cáo Đang Mở Ra",
    exportTitle: "Xuất Báo Cáo",
    exportButton: "Xuất PDF",
    exportHint: "Tải về báo cáo hiện tại từ endpoint xuất file của backend.",
    validationName: "Tên là bắt buộc.",
    validationDate: "Ngày sinh là bắt buộc.",
    validationPlace: "Nơi sinh là bắt buộc.",
    validationQuestion: "Cần có câu hỏi để bắt đầu.",
    importantNote: "Lưu Ý Quan Trọng",
    errorPrefix: "Đã xảy ra lỗi",
    birthTimeLabels: {
      hour: "Giờ",
      minute: "Phút",
      period: "Buổi",
      unknown: "Chưa rõ giờ sinh",
    },
    genderOptions: {
      female: "Nữ",
      male: "Nam",
      non_binary: "Phi nhị nguyên",
      prefer_not_to_say: "Không muốn nêu",
    },
    placeholders: {
      name: "Tên của bạn",
      birthPlace: "Hồ Chí Minh City, Việt Nam",
      question: "Năm nay tôi nên tập trung vào tình cảm, công việc, và phát triển bản thân như thế nào?",
      timeFocus: "Năm nay hoặc 2026-2030",
    },
  },
};

const modes = {
  vedatwin: {
    en: {
      badge: "VedaTwin Reading",
      tagline: "Reflective Vedic astrology, orchestrated by a live AI crew.",
      subtitle:
        "A bilingual Gemini-powered observatory for symbolic Vedic readings, optional image reflection, and streaming multi-agent insight.",
      inputTitle: "Open your Vedic reading",
      inputHint:
        "Enter your details to begin a premium VedaTwin reading. Optional images remain symbolic and are never treated as scientific proof.",
      logsEmpty:
        "Validating input, calculating chart structure, interpreting symbolic patterns, and shaping guidance will appear here in real time.",
      resultEmpty:
        "Your VedaTwin report will unfold here chunk by chunk, then settle into structured sections once the run is complete.",
      footer:
        "Built with Multi-Agent System. Designed like a professional, enhancing quality and ensuring accuracy.",
      modeOptions: {
        vedatwin: {
          title: "VedaTwin Reading",
          description:
            "Vedic-style symbolic reading with chart themes, timing, and reflective guidance.",
        },
        eastern_destiny: {
          title: "Eastern Destiny Reading",
          description:
            "East Asian destiny-style reflection through pillars, elements, and symbolic life patterns.",
        },
      },
    },
    vi: {
      badge: "VedaTwin Reading",
      tagline:
        "Chiêm nghiệm chiêm tinh Vệ Đà được điều phối bởi một nhóm AI đang hoạt động.",
      subtitle:
        "Một đài quan sát Gemini song ngữ cho bản đọc Vệ Đà mang tính biểu tượng, có streaming, có agent, và có lớp an toàn rõ ràng.",
      inputTitle: "Mở bản đọc Vệ Đà",
      inputHint:
        "Nhập thông tin để bắt đầu một bản đọc VedaTwin chỉn chu. Ảnh tải lên chỉ được dùng như đầu vào biểu tượng, không phải bằng chứng khoa học.",
      logsEmpty:
        "Các bước kiểm tra đầu vào, tính lá số, diễn giải biểu tượng, và tạo gợi ý sẽ hiển thị tại đây theo thời gian thực.",
      resultEmpty:
        "Báo cáo VedaTwin sẽ được hiển thị theo từng đoạn nhỏ, sau đó sắp xếp thành các phần dễ đọc khi quá trình hoàn tất.",
      footer:
        "Xây dựng với Multi-Agent System. Được thiết kế như một chuyên gia thật thụ, nâng cao chất lượng và đảm bảo tính chính xác.",
      modeOptions: {
        vedatwin: {
          title: "VedaTwin Reading",
          description:
            "Hệ đọc kiểu Vệ Đà với lá số biểu tượng, nhịp thời gian, và gợi ý chiêm nghiệm.",
        },
        eastern_destiny: {
          title: "Eastern Destiny Reading",
          description:
            "Hệ đọc kiểu Á Đông với trụ mệnh, ngũ hành, và các mẫu đời sống mang tính biểu tượng.",
        },
      },
    },
  },
  eastern_destiny: {
    en: {
      badge: "Eastern Destiny",
      tagline:
        "Elegant Eastern destiny patterns, mapped through symbols, rhythm, and reflective timing.",
      subtitle:
        "A bilingual East Asian-inspired reading mode that explores symbolic pillars, five-element balance, optional visual cues, and streamed reflective guidance.",
      inputTitle: "Explore your Eastern destiny patterns",
      inputHint:
        "Enter your details to open an Eastern Destiny reading shaped by symbolic pillars, five elements, timing, and gentle self-reflection.",
      logsEmpty:
        "Eastern Destiny will map symbolic pillars, read five-element balance, interpret life tendencies, and stream live guidance here.",
      resultEmpty:
        "Your Eastern Destiny report will stream here in real time, then settle into a polished symbolic reading structure.",
      footer:
        "Built as a dual-system AI ritual: VedaTwin for Vedic reflection, Eastern Destiny for East Asian symbolic insight.",
      modeOptions: {
        vedatwin: {
          title: "VedaTwin Reading",
          description:
            "Vedic-style symbolic reading with chart themes, timing, and reflective guidance.",
        },
        eastern_destiny: {
          title: "Eastern Destiny Reading",
          description:
            "East Asian destiny-style reflection through pillars, elements, and symbolic life patterns.",
        },
      },
    },
    vi: {
      badge: "Eastern Destiny",
      tagline:
        "Khám phá mệnh lý Á Đông qua biểu tượng, nhịp vận, và góc nhìn chiêm nghiệm hiện đại.",
      subtitle:
        "Một chế độ đọc song ngữ lấy cảm hứng từ mệnh lý Á Đông, kết hợp trụ biểu tượng, ngũ hành, dấu hiệu hình ảnh tùy chọn, và luồng phản hồi trực tiếp.",
      inputTitle: "Khám phá mẫu hình Eastern Destiny của bạn",
      inputHint:
        "Nhập thông tin để mở bản đọc Eastern Destiny dựa trên trụ biểu tượng, ngũ hành, nhịp thời vận, và sự chiêm nghiệm nhẹ nhàng.",
      logsEmpty:
        "Eastern Destiny sẽ ánh xạ các trụ biểu tượng, đọc thế ngũ hành, diễn giải xu hướng đời sống, và stream gợi ý trực tiếp tại đây.",
      resultEmpty:
        "Báo cáo Eastern Destiny sẽ được stream theo thời gian thực, sau đó ổn định thành một cấu trúc đọc mệnh lý rõ ràng và dễ theo dõi.",
      footer:
        "Được xây dựng như một AI hai hệ đọc: VedaTwin cho chiêm tinh Vệ Đà, Eastern Destiny cho mệnh lý Á Đông mang tính biểu tượng.",
      modeOptions: {
        vedatwin: {
          title: "VedaTwin Reading",
          description:
            "Hệ đọc kiểu Vệ Đà với lá số biểu tượng, nhịp thời gian, và gợi ý chiêm nghiệm.",
        },
        eastern_destiny: {
          title: "Eastern Destiny Reading",
          description:
            "Hệ đọc kiểu Á Đông với trụ mệnh, ngũ hành, và các mẫu đời sống mang tính biểu tượng.",
        },
      },
    },
  },
};

export function getText(language, readingMode = "vedatwin") {
  return {
    ...shared[language],
    ...modes[readingMode][language],
  };
}

export const reportSectionTitles = {
  vedatwin: {
    en: {
      summary: "Quick Summary",
      question_focus: "Main Themes for Your Question",
      interpretation: "Personality and Core Tendencies",
      transit: "Upcoming Period Highlights",
      face: "Facial Reflection",
      palm: "Palm Reflection",
      advisor: "Practical Guidance",
      encouragement: "Final Encouragement",
    },
    vi: {
      summary: "Tóm Tắt Nhanh",
      question_focus: "Chủ Đề Chính Cho Câu Hỏi Của Bạn",
      interpretation: "Tính Cách Và Xu Hướng Nổi Bật",
      transit: "Giai Đoạn Sắp Tới",
      face: "Góc Nhìn Từ Khuôn Mặt",
      palm: "Góc Nhìn Từ Chỉ Tay",
      advisor: "Gợi Ý Thực Tế",
      encouragement: "Lời Nhắn Cuối",
    },
  },
  eastern_destiny: {
    en: {
      summary: "Quick Summary",
      pillars: "Symbolic Pillar Overview",
      elements: "Five-Element Highlights",
      tendencies: "Personality and Life Tendencies",
      question_focus: "Main Themes for Your Question",
      transit: "Upcoming Period",
      face: "Facial Reflection",
      palm: "Palm Reflection",
      advisor: "Practical Guidance",
      reflection_questions: "Reflection Questions",
      encouragement: "Final Encouragement",
    },
    vi: {
      summary: "Tóm Tắt Nhanh",
      pillars: "Trụ Mệnh Và Nền Tảng Biểu Tượng",
      elements: "Ngũ Hành Nổi Bật",
      tendencies: "Xu Hướng Tính Cách Và Đời Sống",
      question_focus: "Chủ Đề Chính Cho Câu Hỏi Của Bạn",
      transit: "Giai Đoạn Sắp Tới",
      face: "Góc Nhìn Từ Khuôn Mặt",
      palm: "Góc Nhìn Từ Chỉ Tay",
      advisor: "Gợi Ý Thực Tế",
      reflection_questions: "Câu Hỏi Tự Chiêm Nghiệm",
      encouragement: "Lời Nhắn Cuối",
    },
  },
};
