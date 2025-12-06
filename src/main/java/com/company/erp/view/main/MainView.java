package com.company.erp.view.main;

import com.company.erp.entity.User;
import com.google.common.base.Strings;
import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.Html;
import com.vaadin.flow.component.avatar.Avatar;
import com.vaadin.flow.component.avatar.AvatarVariant;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.router.Route;
import io.jmix.core.Messages;
import io.jmix.core.usersubstitution.CurrentUserSubstitution;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.app.main.StandardMainView;
import io.jmix.flowui.view.Install;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewComponent;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;

@Route("")
@ViewController(id = "MainView")
@ViewDescriptor(path = "main-view.xml")
public class MainView extends StandardMainView {
    @ViewComponent
    private Html test;
    @Autowired
    private Messages messages;
    @Autowired
    private UiComponents uiComponents;
    @Autowired
    private CurrentUserSubstitution currentUserSubstitution;


    @Subscribe
    public void onInit(final InitEvent event) {
        test.setHtmlContent("<main style=\"font-family: Inter, Roboto, Arial, sans-serif; padding:16px; color:#222;\">\n" +
                "  <style>\n" +
                "    :root{\n" +
                "      --row-h:40px;\n" +
                "      --labels-w:260px;\n" +
                "      --chart-w:920px;\n" +
                "      --accent-planned:#2b9cf3;\n" +
                "      --accent-actual:#f39c12;\n" +
                "      --accent-group:#e9eef6;\n" +
                "    }\n" +
                "    .gantt { display:flex; gap:12px; align-items:flex-start; width:100%; max-width:1200px; }\n" +
                "    .labels { width:var(--labels-w); min-width:var(--labels-w); box-sizing:border-box; }\n" +
                "    .labels .row { height:var(--row-h); line-height:var(--row-h); padding:0 8px; border-bottom:1px dashed #eee; }\n" +
                "    .labels .task { font-weight:700; color:#111; }\n" +
                "    .labels .block { padding-left:12px; color:#444; font-size:0.95em; }\n" +
                "\n" +
                "    .chart-wrap { border:1px solid #efefef; width:var(--chart-w); overflow:auto; }\n" +
                "    .chart-header { display:flex; height:var(--row-h); border-bottom:1px solid #ddd; background:white; }\n" +
                "    .tick { flex:0 0 60px; text-align:center; padding-top:8px; font-size:12px; border-right:1px solid #f5f5f5; box-sizing:border-box; }\n" +
                "    .rows { position:relative; }\n" +
                "    .row { position:relative; height:var(--row-h); border-bottom:1px dashed #f6f6f6; box-sizing:border-box; }\n" +
                "    .group-bg { position:absolute; height:12px; top:14px; border-radius:4px; background:var(--accent-group); opacity:0.8; }\n" +
                "    .bar { position:absolute; height:20px; top:8px; border-radius:4px; background:var(--accent-planned); color:white; display:flex; align-items:center; padding:0 8px; font-size:12px; box-shadow:0 1px 0 rgba(0,0,0,0.06); overflow:hidden; white-space:nowrap; text-overflow:ellipsis; box-sizing:border-box; }\n" +
                "    .bar.actual { background:transparent; border:2px dashed var(--accent-actual); color:var(--accent-actual); }\n" +
                "    .legend { margin-top:12px; font-size:13px; }\n" +
                "    .legend .item { display:inline-flex; gap:8px; align-items:center; margin-right:16px; }\n" +
                "    .sw { width:22px; height:12px; border-radius:3px; display:inline-block; }\n" +
                "    .sw.group { background:var(--accent-group); }\n" +
                "    .sw.planned { background:var(--accent-planned); }\n" +
                "    .sw.actual { border:2px dashed var(--accent-actual); background:transparent; }\n" +
                "    /* responsive small */\n" +
                "    @media (max-width:1024px){\n" +
                "      :root{ --chart-w:720px; }\n" +
                "    }\n" +
                "  </style>\n" +
                "\n" +
                "  <h3 style=\"margin:0 0 12px 0\">Мини-Гант (статический пример)</h3>\n" +
                "\n" +
                "  <div class=\"gantt\">\n" +
                "    <!-- labels -->\n" +
                "    <div class=\"labels\" aria-hidden=\"true\">\n" +
                "      <div class=\"row task\">Task 1 — Подготовка</div>\n" +
                "      <div class=\"row block\">Анализ требований</div>\n" +
                "      <div class=\"row block\">Прототип</div>\n" +
                "\n" +
                "      <div class=\"row task\">Task 2 — Разработка</div>\n" +
                "      <div class=\"row block\">Архитектура</div>\n" +
                "      <div class=\"row block\">Модуль A</div>\n" +
                "\n" +
                "      <div class=\"row task\">Task 3 — Тестирование</div>\n" +
                "      <div class=\"row block\">Unit тесты</div>\n" +
                "      <div class=\"row block\">Интеграция</div>\n" +
                "    </div>\n" +
                "\n" +
                "    <!-- chart -->\n" +
                "    <div class=\"chart-wrap\" role=\"img\" aria-label=\"Gantt chart preview\">\n" +
                "      <!-- header (ticks) -->\n" +
                "      <div class=\"chart-header\" aria-hidden=\"true\">\n" +
                "        <div class=\"tick\">2025-01-01</div>\n" +
                "        <div class=\"tick\">2025-01-08</div>\n" +
                "        <div class=\"tick\">2025-01-15</div>\n" +
                "        <div class=\"tick\">2025-01-22</div>\n" +
                "        <div class=\"tick\">2025-01-29</div>\n" +
                "        <div class=\"tick\">2025-02-05</div>\n" +
                "        <div class=\"tick\">2025-02-12</div>\n" +
                "        <div class=\"tick\">2025-02-19</div>\n" +
                "        <div class=\"tick\">2025-02-26</div>\n" +
                "      </div>\n" +
                "\n" +
                "      <div class=\"rows\" style=\"min-width:720px;\">\n" +
                "        <!-- Task1 group row -->\n" +
                "        <div class=\"row\" style=\"height:var(--row-h);\">\n" +
                "          <!-- group background: left 5% width 20% -->\n" +
                "          <div class=\"group-bg\" style=\"left:5%; width:28%;\"></div>\n" +
                "        </div>\n" +
                "\n" +
                "        <!-- Task1 block1: planned 8%->18% -->\n" +
                "        <div class=\"row\">\n" +
                "          <div class=\"bar\" style=\"left:8%; width:10%;\">Анализ требований</div>\n" +
                "        </div>\n" +
                "\n" +
                "        <!-- Task1 block2: planned 20%->36%, actual ended later 40% -->\n" +
                "        <div class=\"row\">\n" +
                "          <div class=\"bar\" style=\"left:20%; width:16%;\">Прототип</div>\n" +
                "          <div class=\"bar actual\" style=\"left:20%; width:20%;\">Прототип (факт)</div>\n" +
                "        </div>\n" +
                "\n" +
                "        <!-- Task2 group row -->\n" +
                "        <div class=\"row\">\n" +
                "          <div class=\"group-bg\" style=\"left:18%; width:45%;\"></div>\n" +
                "        </div>\n" +
                "\n" +
                "        <!-- Task2 block1 -->\n" +
                "        <div class=\"row\">\n" +
                "          <div class=\"bar\" style=\"left:18%; width:12%;\">Архитектура</div>\n" +
                "        </div>\n" +
                "\n" +
                "        <!-- Task2 block2 -->\n" +
                "        <div class=\"row\">\n" +
                "          <div class=\"bar\" style=\"left:31%; width:32%;\">Модуль A</div>\n" +
                "        </div>\n" +
                "\n" +
                "        <!-- Task3 group row -->\n" +
                "        <div class=\"row\">\n" +
                "          <div class=\"group-bg\" style=\"left:62%; width:30%;\"></div>\n" +
                "        </div>\n" +
                "\n" +
                "        <!-- Task3 block1 (actual finished earlier) -->\n" +
                "        <div class=\"row\">\n" +
                "          <div class=\"bar\" style=\"left:62%; width:10%;\">Unit тесты</div>\n" +
                "          <div class=\"bar actual\" style=\"left:62%; width:8%;\">Unit тесты (факт)</div>\n" +
                "        </div>\n" +
                "\n" +
                "        <!-- Task3 block2 -->\n" +
                "        <div class=\"row\">\n" +
                "          <div class=\"bar\" style=\"left:73%; width:18%;\">Интеграция</div>\n" +
                "        </div>\n" +
                "      </div>\n" +
                "    </div>\n" +
                "  </div>\n" +
                "\n" +
                "  <div class=\"legend\" aria-hidden=\"true\">\n" +
                "    <span class=\"item\"><span class=\"sw group\"></span> Задача (граница по блокам)</span>\n" +
                "    <span class=\"item\"><span class=\"sw planned\"></span> Плановый интервал</span>\n" +
                "    <span class=\"item\"><span class=\"sw actual\"></span> Фактический интервал (пунктир)</span>\n" +
                "  </div>\n" +
                " <a href=\"https://www.w3schools.com/\">Visit W3Schools.com!</a>\n" +
                "</main>\n");
    }

    @Install(to = "userMenu", subject = "buttonRenderer")
    private Component userMenuButtonRenderer(final UserDetails userDetails) {
        if (!(userDetails instanceof User user)) {
            return null;
        }

        String userName = generateUserName(user);

        Div content = uiComponents.create(Div.class);
        content.setClassName("user-menu-button-content");

        Avatar avatar = createAvatar(userName);

        Span name = uiComponents.create(Span.class);
        name.setText(userName);
        name.setClassName("user-menu-text");

        content.add(avatar, name);

        if (isSubstituted(user)) {
            Span subtext = uiComponents.create(Span.class);
            subtext.setText(messages.getMessage("userMenu.substituted"));
            subtext.setClassName("user-menu-subtext");

            content.add(subtext);
        }

        return content;
    }

    @Install(to = "userMenu", subject = "headerRenderer")
    private Component userMenuHeaderRenderer(final UserDetails userDetails) {
        if (!(userDetails instanceof User user)) {
            return null;
        }

        Div content = uiComponents.create(Div.class);
        content.setClassName("user-menu-header-content");

        String name = generateUserName(user);

        Avatar avatar = createAvatar(name);
        avatar.addThemeVariants(AvatarVariant.LUMO_LARGE);

        Span text = uiComponents.create(Span.class);
        text.setText(name);
        text.setClassName("user-menu-text");

        content.add(avatar, text);

        if (name.equals(user.getUsername())) {
            text.addClassNames("user-menu-text-subtext");
        } else {
            Span subtext = uiComponents.create(Span.class);
            subtext.setText(user.getUsername());
            subtext.setClassName("user-menu-subtext");

            content.add(subtext);
        }

        return content;
    }

    private Avatar createAvatar(String fullName) {
        Avatar avatar = uiComponents.create(Avatar.class);
        avatar.setName(fullName);
        avatar.getElement().setAttribute("tabindex", "-1");
        avatar.setClassName("user-menu-avatar");

        return avatar;
    }

    private String generateUserName(User user) {
        String userName = String.format("%s %s",
                        Strings.nullToEmpty(user.getFirstName()),
                        Strings.nullToEmpty(user.getLastName()))
                .trim();

        return userName.isEmpty() ? user.getUsername() : userName;
    }

    private boolean isSubstituted(User user) {
        UserDetails authenticatedUser = currentUserSubstitution.getAuthenticatedUser();
        return user != null && !authenticatedUser.getUsername().equals(user.getUsername());
    }
}
