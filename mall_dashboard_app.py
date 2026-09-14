        with tab_entry:
            st.markdown("### 🚗 Driving to Parking Spot")

            fig_entry = render_rooftop_parking_map(
                assigned_slot=assigned_slot,
                route_path=entry_path,
                current_lang=st.session_state.lang,
            )
            st.plotly_chart(fig_entry, use_container_width=True)

            if entry_path:
                entry_summary = compute_route_summary(entry_path)
                st.markdown("---")
                st.subheader(t["parking_route_summary"])

                p_col1, p_col2, p_col3 = st.columns(3)
                p_col1.metric(
                    t["dist_to_spot"], f"{entry_summary['total_distance']} m"
                )
                p_col2.metric(
                    t["floors_to_ascend"], entry_summary["floors_crossed"]
                )
                p_col3.metric(t["total_steps"], entry_summary["steps"])

                st.markdown("---")
                st.subheader(t["parking_turn_by_turn"])
                entry_steps = generate_detailed_directions(
                    entry_path, MULTI_CAD_NODES, lang=st.session_state.lang
                )

                for step_info in entry_steps:
                    col_icon, col_text = st.columns([0.1, 0.9])
                    with col_icon:
                        st.markdown(f"### {step_info['icon']}")
                    with col_text:
                        st.markdown(f"**{t['step_lbl']} {step_info['step']}**")
                        st.markdown(step_info["text"])
                    st.divider()

        with tab_exit:
            st.markdown("### 🚪 Leaving Parking Spot to Driveway Exit")

            fig_exit = render_rooftop_parking_map(
                assigned_slot=assigned_slot,
                route_path=exit_path,
                current_lang=st.session_state.lang,
            )
            st.plotly_chart(fig_exit, use_container_width=True)

            if exit_path:
                exit_summary = compute_route_summary(exit_path)
                st.markdown("---")
                st.subheader(t["parking_route_summary"])

                e_col1, e_col2, e_col3 = st.columns(3)
                e_col1.metric(
                    t["dist_to_spot"], f"{exit_summary['total_distance']} m"
                )
                e_col2.metric(
                    t["floors_to_ascend"], exit_summary["floors_crossed"]
                )
                e_col3.metric(t["total_steps"], exit_summary["steps"])

                st.markdown("---")
                st.subheader(t["parking_turn_by_turn"])
                exit_steps = generate_detailed_directions(
                    exit_path, MULTI_CAD_NODES, lang=st.session_state.lang
                )

                for step_info in exit_steps:
                    col_icon, col_text = st.columns([0.1, 0.9])
                    with col_icon:
                        st.markdown(f"### {step_info['icon']}")
                    with col_text:
                        st.markdown(f"**{t['step_lbl']} {step_info['step']}**")
                        st.markdown(step_info["text"])
                    st.divider()

    else:
        st.error("⚠️ No available parking spots found on the Rooftop layer.")
        fig_parking = render_rooftop_parking_map(
            assigned_slot=None,
            route_path=[],
            current_lang=st.session_state.lang,
        )
        st.plotly_chart(fig_parking, use_container_width=True)

# ==============================================================================
# 7. Footer
# ==============================================================================

def render_system_footer():
    st.markdown("---")
    foot_col1, foot_col2, foot_col3 = st.columns(3)

    with foot_col1:
        st.caption("🏢 **System Architecture:** 3D Theta* Pathfinding Engine")
    with foot_col2:
        st.caption(
            "📐 **Vector Processing:** FloorPlanCAD Parser (DXF/SVG Topology)"
        )
    with foot_col3:
        st.caption("🌐 **Localization:** Active Multilingual Engine")

if __name__ == "__main__":
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
    render_system_footer()
